import json
import math
import os
from collections import deque
from flatpack.datasets import TextDataset
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.optim.lr_scheduler import LambdaLR


class Transformer(nn.Module):
    def __init__(self, embed_size, hidden_size, num_layers, vocab_size=None, nhead=8, dropout=0.1, device='cpu'):
        super(Transformer, self).__init__()
        self.embed_size = embed_size
        self.device = device
        self.embedding = nn.Embedding(vocab_size, embed_size).to(device) if vocab_size else None
        self.layer_norm = nn.LayerNorm(embed_size).to(device)
        self.dropout = nn.Dropout(dropout).to(device)
        self.transformer_decoder = nn.TransformerDecoder(
            nn.TransformerDecoderLayer(embed_size, nhead, hidden_size, dropout=dropout), num_layers).to(device)
        self.fc = nn.Linear(embed_size, vocab_size).to(device) if vocab_size else None
        self.positional_encoding = self.add_positional_encoding(
            torch.zeros(1, 5000, self.embed_size).to(device)).detach()

    def add_positional_encoding(self, x):
        position = torch.arange(0, x.size(1)).unsqueeze(0).to(x.device)
        div_term = torch.exp(torch.arange(0, self.embed_size, 2) * -(math.log(10000.0) / self.embed_size)).to(x.device)
        pe = torch.zeros(x.size(1), self.embed_size).to(x.device)
        pe[:, 0::2], pe[:, 1::2] = torch.sin(position * div_term), torch.cos(position * div_term)
        return pe.unsqueeze(0)

    def forward(self, x):
        if not self.embedding or not self.fc:
            raise ValueError(
                "Either embedding or fully connected layer is not initialized. Ensure vocab_size is provided or loaded.")
        x = self.embedding(x) * math.sqrt(self.embed_size)
        x = self.layer_norm(x + self.positional_encoding[:, :x.size(1), :])
        x = self.dropout(x)
        return self.fc(self.transformer_decoder(x, x))

    def load_vocab_size(self, save_dir):
        with open(os.path.join(save_dir, 'char_to_index.json'), 'r') as f:
            char_to_index = json.load(f)
        self.embedding = nn.Embedding(len(char_to_index), self.embed_size).to(self.device)
        self.fc = nn.Linear(self.embed_size, len(char_to_index)).to(self.device)

    @classmethod
    def train_model(cls, indexed_text, vocab_size, seq_length, embed_size, hidden_size, num_layers, epochs, batch_size,
                    device, nhead=8, dropout=0.1, warmup_steps=5000):
        dataloader = DataLoader(TextDataset(indexed_text, seq_length=seq_length), batch_size=batch_size, shuffle=True)
        model = cls(embed_size, hidden_size, num_layers, vocab_size, nhead, dropout, device).to(device)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.AdamW(model.parameters(), lr=5e-4, betas=(0.9, 0.98), eps=1e-9, weight_decay=0.01)
        warmup_scheduler = LambdaLR(optimizer, lambda step: min((step + 1) / warmup_steps, 1.0))

        for epoch in range(epochs):
            total_loss, total_accuracy, total_batches = 0.0, 0.0, 0
            for data, target in dataloader:
                inputs, targets = data.to(device), target.to(device)
                outputs = model(inputs)
                loss = criterion(outputs.view(-1, vocab_size), targets.view(-1))
                optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                optimizer.step()
                warmup_scheduler.step()

                total_loss += loss.item()
                total_accuracy += (torch.max(outputs, 2)[1] == targets).float().sum().item() / (
                        targets.size(0) * targets.size(1))
                total_batches += 1

            print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss / total_batches:.4f}, "
                  f"Accuracy: {total_accuracy / total_batches:.4f}, Perplexity: {math.exp(total_loss / total_batches):.2f}")

        return {'model': model}

    def generate_text(self, save_dir, start_sequence="To be, or not to be", generate_length=1024, temperature=1.0,
                      device=None):
        with open(os.path.join(save_dir, 'char_to_index.json'), 'r') as f_char, \
                open(os.path.join(save_dir, 'index_to_char.json'), 'r') as f_index:
            char_to_index, index_to_char = json.load(f_char), json.load(f_index)

        input_sequence = deque(maxlen=len(start_sequence))
        [input_sequence.append(char_to_index[char]) for char in start_sequence]

        self.to(device).eval()
        generated_text = start_sequence
        with torch.no_grad():
            for _ in range(generate_length):
                input_tensor = torch.tensor(list(input_sequence)).long().unsqueeze(0).to(device)
                output = self(input_tensor)
                next_index = torch.multinomial(F.softmax(output[0, -1] / temperature, dim=0), 1).item()
                generated_text += index_to_char[str(next_index)]
                input_sequence.append(next_index)

        return generated_text

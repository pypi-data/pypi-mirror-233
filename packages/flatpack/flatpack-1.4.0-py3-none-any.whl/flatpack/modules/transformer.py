import json
import math
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from flatpack.datasets import TextDataset
from torch.utils.data import DataLoader, Dataset
from torch.optim.lr_scheduler import CosineAnnealingLR


def seed_everything(seed: int):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True


class Transformer(nn.Module):
    def __init__(self, embed_size, hidden_size, num_layers, vocab_size=None, nhead=8, dropout=0.1):
        super(Transformer, self).__init__()
        self.embed_size = embed_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.embedding = nn.Embedding(vocab_size, embed_size) if vocab_size is not None else None
        self.dropout = nn.Dropout(dropout)
        self.transformer_decoder = nn.TransformerDecoder(
            nn.TransformerDecoderLayer(embed_size, nhead, hidden_size, dropout=dropout), num_layers)
        self.fc = nn.Linear(embed_size, vocab_size) if vocab_size is not None else None

    def forward(self, x):
        if self.embedding is None or self.fc is None:
            raise ValueError("vocab_size is not loaded")
        x = self.embedding(x)
        x = self.dropout(x)
        output = self.transformer_decoder(x, x)
        return self.fc(output)

    @staticmethod
    def load_torch_model(model_path):
        return torch.load(model_path)

    def load_vocab_size(self, save_dir):
        with open(os.path.join(save_dir, 'char_to_index.json'), 'r') as f:
            char_to_index = json.load(f)
        self.vocab_size = len(char_to_index)
        self.embedding = nn.Embedding(self.vocab_size, self.embed_size)
        self.fc = nn.Linear(self.embed_size, self.vocab_size)

    @classmethod
    def train_model(cls, indexed_text, vocab_size, seq_length, embed_size, hidden_size, num_layers, epochs,
                    batch_size,
                    device, nhead=8, dropout=0.1):
        dataset = TextDataset(indexed_text, seq_length=seq_length)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        model = cls(embed_size, hidden_size, num_layers, vocab_size, nhead)
        model.to(device)

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.AdamW(model.parameters())

        total_loss = 0.0
        total_accuracy = 0.0
        total_batches = 0

        learning_rate = 5e-4
        scheduler = CosineAnnealingLR(optimizer, T_max=len(dataloader) * epochs, eta_min=1e-5)

        for epoch in range(epochs):
            for batch_idx, (data, target) in enumerate(dataloader):
                inputs, targets = data.to(device), target.to(device)
                outputs = model(inputs)
                loss = criterion(outputs.view(-1, vocab_size), targets.view(-1))

                optimizer.zero_grad()
                loss.backward()

                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                optimizer.step()
                scheduler.step()

                _, predicted = torch.max(outputs, 2)
                correct = (predicted == targets).float()
                accuracy = correct.sum().item() / (targets.size(0) * targets.size(1))
                total_loss += loss.item()
                total_accuracy += accuracy
                total_batches += 1

            average_loss = total_loss / total_batches
            average_accuracy = total_accuracy / total_batches
            perplexity = math.exp(average_loss)

            print(
                f"Epoch {epoch + 1}/{epochs}, Loss: {average_loss:.4f}, Accuracy: {average_accuracy:.4f}, Perplexity: {perplexity:.2f}")

        return {'model': model}

    def generate_text(self, save_dir, start_sequence="To be, or not to be", generate_length=1024, temperature=1.0,
                      device=None):
        with open(os.path.join(save_dir, 'char_to_index.json'), 'r') as f:
            char_to_index = json.load(f)

        with open(os.path.join(save_dir, 'index_to_char.json'), 'r') as f:
            index_to_char = json.load(f)

        input_sequence = [char_to_index[char] for char in start_sequence]
        input_tensor = torch.tensor(input_sequence).long().unsqueeze(0)

        if device is not None:
            input_tensor = input_tensor.to(device)
            self.to(device)

        generated_text = start_sequence
        self.eval()

        with torch.no_grad():
            for _ in range(generate_length):
                output = self(input_tensor)
                probabilities = F.softmax(output[0, -1] / temperature, dim=0)
                next_index = torch.multinomial(probabilities, 1).item()
                next_token = index_to_char[str(next_index)]

                generated_text += next_token
                input_sequence = input_sequence[1:] + [next_index]
                input_tensor = torch.tensor(input_sequence).long().unsqueeze(0)

                if device is not None:
                    input_tensor = input_tensor.to(device)

        return generated_text

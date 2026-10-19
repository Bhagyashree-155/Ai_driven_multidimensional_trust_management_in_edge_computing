import torch
import torch.nn as nn

class TransformerModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(3, 1)

    def forward(self, x):
        return torch.sigmoid(self.fc(x))

model = TransformerModel()

def predict(features):
    x = torch.tensor(features, dtype=torch.float32)
    return model(x).item()
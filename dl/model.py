import torch
from torch import nn

class PerioMLP(nn.Module):
  def __init__(self, input_dim):
    super().__init__()

    self.network = nn.Sequential(
      nn.Linear(input_dim, 32),
      nn.ReLLU(),

      nn.Linear(32, 16),
      nn.ReLU(),

      nn.Dropout(p=0.2),
      
      nn.Linear(16, 1) 
    )

  def forward(self, x):
    return self.network(x)  
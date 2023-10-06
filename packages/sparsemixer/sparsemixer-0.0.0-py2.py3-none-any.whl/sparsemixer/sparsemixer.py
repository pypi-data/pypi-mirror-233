import torch
import torch.nn as nn
import torch.nn.functional as F

class SparseMixer(nn.Module):
    def __init__(self, num_experts, embed_dim, compute_balance_loss=False, jitter_eps=0.1):
        super(SparseMixer, self).__init__()

    def forward(self, logits):
        raise "implementation under release review, will release asap, stay tuned!"

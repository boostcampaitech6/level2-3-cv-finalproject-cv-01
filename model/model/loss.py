import torch
import torch.nn as nn
import torch.nn.functional as F



def nll_loss(output, target):
    return F.nll_loss(output, target)

def bce_loss(output, target):
    output = output.to(torch.float64)
    target = F.one_hot(target, num_classes=2).to(torch.float64)
    criterion = nn.BCELoss()

    return criterion(output, target)

def cross_entropy_loss(outputs, targets):
    return F.cross_entropy(outputs, targets)
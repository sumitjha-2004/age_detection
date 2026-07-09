import torch
import torch.nn as nn
from torchvision import models

classes = [
    "0-2",
    "3-9",
    "10-19",
    "20-29",
    "30-39",
    "40-49",
    "50-59",
    "60-69",
    "more than 70"
]

def load_model():
    model = models.resnet18(weights=None)
    model.fc = nn.Sequential(
        nn.Dropout(0.5),
        nn.Linear(model.fc.in_features, 9)
    )
    state_dict = torch.load(
        "resnet18_age_detection.pth",
        map_location="cpu",
        weights_only=True
    )
    model.load_state_dict(state_dict)
    model.eval()
    return model
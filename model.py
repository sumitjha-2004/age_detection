import torch
import torch.nn as nn
from torchvision import models

classes = [
    "18-20",
    "21-30",
    "31-40",
    "41-50",
    "51-60"
]

def load_model():

    model = models.resnet18(weights=None)

    model.fc = nn.Sequential(
        nn.Dropout(0.5),
        nn.Linear(model.fc.in_features, 5)
    )

    state_dict = torch.load(
        "age_classifier.pth",
        map_location="cpu",
        weights_only=True
    )
    model.load_state_dict(state_dict)

    model.eval()
    return model

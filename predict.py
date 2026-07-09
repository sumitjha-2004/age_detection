import torch
from PIL import Image
from torchvision import transforms

from model import load_model, classes

model = load_model()

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485,0.456,0.406],
        [0.229,0.224,0.225]
    )
])

def predict(image):

    image = transform(image)
    image = image.unsqueeze(0)

    with torch.no_grad():
        output = model(image)
        probability = torch.softmax(output, 1)[0]  # shape: (9,)
        confidence, pred = torch.max(probability, 0)

    distribution = {
        classes[i]: round(probability[i].item() * 100, 2)
        for i in range(len(classes))
    }

    return classes[pred.item()], confidence.item() * 100, distribution
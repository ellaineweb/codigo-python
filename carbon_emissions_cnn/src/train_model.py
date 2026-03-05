import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
from src.config import CLASSIFIED_IMAGE_DIR, MODEL_PATH


def train_model(epochs=100):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])

    dataset = datasets.ImageFolder(CLASSIFIED_IMAGE_DIR, transform=transform)
    loader = DataLoader(dataset, batch_size=4, shuffle=True)

    model = models.resnet18(pretrained=True)
    model.fc = nn.Linear(model.fc.in_features, 3)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for imgs, labels in loader:
            imgs, labels = imgs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(imgs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Época {epoch+1}, Loss: {total_loss:.4f}")

    torch.save(model.state_dict(), MODEL_PATH)

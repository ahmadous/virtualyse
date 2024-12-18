import requests
import torch
from torchvision import models, transforms
from PIL import Image

# Charger le modèle ResNet50 pré-entraîné
model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
model.eval()  # Mettre le modèle en mode évaluation

# Transformer pour prétraiter les images avant de les passer dans le modèle
preprocess = transforms.Compose([
    transforms.Resize(256),                 # Redimensionner à 256x256
    transforms.CenterCrop(224),             # Découper au centre pour obtenir une image 224x224
    transforms.ToTensor(),                  # Convertir en tenseur PyTorch
    transforms.Normalize(                   # Normaliser avec les valeurs utilisées par ImageNet
        mean=[0.485, 0.456, 0.406], 
        std=[0.229, 0.224, 0.225]
    ),
])

# Charger les labels d'ImageNet
LABELS_URL = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
imagenet_labels = requests.get(LABELS_URL).json()

# Fonction d'inférence
def predict_image(image_path):
    try:
        # Charger l'image
        image = Image.open(image_path).convert("RGB")
        image_tensor = preprocess(image).unsqueeze(0)  # Ajouter une dimension batch

        # Passer l'image dans le modèle
        with torch.no_grad():
            outputs = model(image_tensor)
            _, predicted_idx = torch.max(outputs, 1)  # Obtenir l'indice de la classe prédite

        # Retourner le label associé
        predicted_label = imagenet_labels[predicted_idx.item()]
        return predicted_label
    except Exception as e:
        raise ValueError(f"Erreur lors de l'inférence : {e}")

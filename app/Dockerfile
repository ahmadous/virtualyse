FROM python:3.9-slim

# Installer les dépendances
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir --no-deps -r requirements.txt --prefer-binary

# Exposer le port 8000
EXPOSE 8000

# Commande pour démarrer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

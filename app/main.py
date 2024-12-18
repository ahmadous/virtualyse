from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from inference import predict_image  # Assurez-vous que `predict_image` est défini dans `inference.py`
import mysql.connector
from mysql.connector import Error

# Initialisation de l'application FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Remplacez "*" par votre URL frontend si nécessaire
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dossier pour les fichiers uploadés
UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Fonction pour établir une connexion MySQL
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",  # XAMPP MySQL tourne sur localhost
            user="root",       # Utilisateur par défaut de XAMPP
            password="",       # Mot de passe par défaut est vide pour root
            database="image_db"
        )
        if connection.is_connected():
            print("Connexion réussie à MySQL (XAMPP)")
        return connection
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL : {e}")
        return None

# Route pour traiter une image et stocker la prédiction
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Enregistrer le fichier
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Vérifier et prédire
        prediction = predict_image(file_path)
        return {"file_name": file.filename, "prediction": prediction}
    except ValueError as ve:
        # Gérer les erreurs de type fichier non valide
        logging.error(f"Erreur : {ve}")
        return JSONResponse(content={"error": str(ve)}, status_code=400)
    except Exception as e:
        # Gérer les erreurs générales
        logging.error(f"Erreur serveur : {e}")
        return JSONResponse(content={"error": "Erreur interne du serveur"}, status_code=500)

# Route pour récupérer toutes les prédictions
@app.get("/predictions")
async def get_predictions():
    try:
        # Connecter à la base de données et récupérer les prédictions
        connection = create_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM predictions ORDER BY created_at DESC"
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            connection.close()

        # Retourner les prédictions sous forme JSON
        return {"predictions": results}
    except Exception as e:
        return {"error": str(e)}

# Route pour vérifier que l'API est en ligne
@app.get("/")
async def root():
    return {"message": "API en ligne. Utilisez /predict pour uploader une image."}
import uvicorn
if __name__ == "__main__":
    print("API FastAPI en cours d'exécution sur http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)

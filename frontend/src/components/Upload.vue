<template>
<div class="upload-container">
    <h1>Uploader une Image pour la Prédiction</h1>

    <!-- Input pour téléverser un fichier -->
    <input type="file" @change="handleFileUpload" />
    <button :disabled="!file" @click="submitFile">Envoyer</button>

    <!-- Indicateur de chargement -->
    <div v-if="loading" class="loading">
    <p>Traitement en cours...</p>
    </div>

    <!-- Affichage des résultats -->
    <div v-if="prediction">
    <h2>Résultat de la Prédiction :</h2>
    <p><strong>Nom du fichier :</strong> {{ fileName }}</p>
    <p><strong>Prédiction :</strong> {{ prediction }}</p>
    </div>

    <!-- Aperçu du fichier sélectionné -->
    <div v-if="preview">
    <h3>Aperçu :</h3>
    <img v-if="isImage" :src="preview" alt="Aperçu" />
    <p v-else>Ce format n'est pas supporté pour un aperçu.</p>
    </div>

    <!-- Affichage des erreurs -->
    <div v-if="error" class="error">
    <p>Erreur : {{ error }}</p>
    </div>
</div>
</template>

<script>
    export default {
    data() {
        return {
        file: null,         // Fichier sélectionné
        preview: null,      // URL d'aperçu pour l'image
        prediction: null,   // Prédiction retournée par le backend
        fileName: null,     // Nom du fichier envoyé
        error: null,        // Message d'erreur
        loading: false,     // Indicateur de chargement
        };
    },
    computed: {
        isImage() {
        // Vérifier si le fichier est une image
        return this.file && this.file.type.startsWith("image/");
        },
    },
    methods: {
        // Gestion de la sélection d'un fichier
        handleFileUpload(event) {
        this.file = event.target.files[0]; // Récupérer le fichier sélectionné
        this.error = null;
        this.prediction = null;

        if (this.file) {
            const validFormats = ["image/png", "image/jpeg", "image/jpg"];
            if (!validFormats.includes(this.file.type)) {
            this.error = "Seuls les formats PNG et JPEG sont acceptés.";
            this.file = null;
            this.preview = null;
            return;
            }
            // Créer un aperçu de l'image
            this.preview = URL.createObjectURL(this.file);
        }
        },
        // Gestion de l'envoi du fichier au backend
        async submitFile() {
        if (!this.file) {
            this.error = "Veuillez sélectionner un fichier avant de l'envoyer.";
            return;
        }

        this.loading = true; // Activer l'indicateur de chargement
        this.error = null;
        this.prediction = null;

        const formData = new FormData();
        formData.append("file", this.file);

        try {
            const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            body: formData,
            });

            if (!response.ok) {
            const errorData = await response.json(); // Lire les détails de l'erreur
            throw new Error(errorData.error || "Erreur inconnue côté serveur.");
            }

            const data = await response.json();
            this.prediction = data.prediction; // Stocker la prédiction
            this.fileName = data.file_name;   // Stocker le nom du fichier
        } catch (err) {
            console.error("Erreur :", err);
            this.error = err.message || "Une erreur inconnue s'est produite.";
        } finally {
            this.loading = false; // Désactiver l'indicateur de chargement
        }
        },
    },
};
</script>

<style scoped>
    .upload-container {
        max-width: 600px;
        margin: 0 auto;
        text-align: center;
        padding: 20px;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #f9f9f9;
    }
    input[type="file"] {
        margin: 20px 0;
    }
    button {
        padding: 10px 20px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
    }
    button:disabled {
        background-color: #ccc;
        cursor: not-allowed;
    }
    button:hover:not(:disabled) {
        background-color: #0056b3;
    }
    .loading {
        margin: 20px 0;
        color: #007bff;
    }

    .error {
        margin: 20px 0;
        color: red;
    }
    img {
        margin-top: 20px;
        max-width: 100%;
        height: auto;
        border: 1px solid #ddd;
        border-radius: 5px;
    }
</style>

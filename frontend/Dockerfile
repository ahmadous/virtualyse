# Étape 1 : Construire l'application Vue.js
FROM node:18-alpine AS build  
#Vérifiez que la version de Node.js est correcte
WORKDIR /app

# Copiez les fichiers package.json et package-lock.json
COPY package*.json ./

# Installez les dépendances
RUN npm install

# Copiez le reste des fichiers
COPY . .

# Construisez l'application
RUN npm run build

# Étape 2 : Servir avec Nginx
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

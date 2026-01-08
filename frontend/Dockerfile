# Etapa 1 — Build do React
FROM node:18 AS build

WORKDIR /app

COPY package*.json ./
RUN npm install --legacy-peer-deps

COPY . .
RUN npm run build

# Etapa 2 — Nginx para servir a build
FROM nginx:stable-alpine

# Remove configuração default
RUN rm /etc/nginx/conf.d/default.conf

# Copia nossa config otimizada
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copia os arquivos do build final
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
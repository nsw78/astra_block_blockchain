# Build stage
FROM node:18-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

# Frontend talks to itself via nginx reverse proxy — no hardcoded backend URL
ENV VITE_ASTRA_API_URL=

# Use vite build only (Vite handles TS transpilation via esbuild)
RUN npx vite build

# Production stage
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

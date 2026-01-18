# Build stage
FROM node:18-alpine AS build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies with cache
RUN --mount=type=cache,target=/root/.npm \
    npm install

# Copy source code
COPY . .

# Set API URL for production (backend service name)
ENV VITE_ASTRA_API_URL=http://astra:8080

# Build the app
RUN npm run build

# Debug: list dist contents
RUN ls -la /app/dist/ && ls -la /app/dist/assets/

# Production stage
FROM nginx:alpine

# Copy built app to nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Debug: list nginx html contents
RUN ls -la /usr/share/nginx/html/ && ls -la /usr/share/nginx/html/assets/

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
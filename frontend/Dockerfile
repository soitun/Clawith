FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci --registry https://registry.npmmirror.com
COPY . .
RUN npm run build

FROM nginx:alpine
# Create non-root user
RUN apk add --no-cache dumb-init && \
    addgroup -g 1001 -S nginx && \
    adduser -S nginx -u 1001 -G nginx

COPY --from=build --chown=nginx:nginx /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

USER nginx

EXPOSE 3000
ENTRYPOINT ["dumb-init", "nginx", "-g", "daemon off;"]

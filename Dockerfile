FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
COPY installer.bash /usr/share/nginx/html/installer.bash

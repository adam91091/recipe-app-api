# base image - why we select unprivileged?
# By default, nginx runs image as root user, which is not best for security
# This type of image may be executed as non-root user
# it gives unprivileged instance of NGINX
FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="adam91091"

# Copy files into the image location
# nginx looks for the files in /etc/nginx/* location
COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

# Default values for environment variables
# It can be overriden during running a service
ENV LISTEN_PORT=8000
ENV APP_HOST=app
ENV APP_PORT=9000

# switch to root user to setup image
USER root

# do administration work as root user
# create empty default.conf and set rights
RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

VOLUME /vol/static

# switch to nginx user - this user is available in nginx base image.
USER nginx

CMD ["/run.sh"]

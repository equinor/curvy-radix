# https://hub.docker.com/r/frolvlad/alpine-python-machinelearning/
FROM frolvlad/alpine-python-machinelearning

LABEL description "Nginx(HTTP Server) + uWSGI + Flask based on Alpine Linux and managed by Supervisord"

# Proxy configuration to be used when running locally. Must be commented out when deploying to Radix.
# ARG HTTP_PROXY=http://www-proxy.statoil.no:80
# ARG HTTPS_PROXY=http://www-proxy.statoil.no:80

RUN apk add \
    nginx \
    uwsgi \
    uwsgi-python3 \
    git \
    supervisor && \
    pip3 install --upgrade pip setuptools && \
    pip3 install flask && \
    pip3 install --no-cache-dir git+https://github.com/equinor/curvy.git@master#egg=curvy && \
    rm /etc/nginx/conf.d/default.conf && \
    rm -r /root/.cache

# Copy the Nginx global conf
COPY nginx.conf /etc/nginx/
# Copy the Flask Nginx site conf
COPY flask-site-nginx.conf /etc/nginx/conf.d/
# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY uwsgi.ini /etc/uwsgi/
# Custom Supervisord config
COPY supervisord.conf /etc/supervisord.conf

# Add demo app
COPY ./app /app
WORKDIR /app

EXPOSE 80

CMD ["/usr/bin/supervisord","-c","/etc/supervisord.conf"]
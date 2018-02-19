FROM nginx:1.13.8

RUN rm /etc/nginx/nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/
COPY bfex.conf /etc/nginx/conf.d/

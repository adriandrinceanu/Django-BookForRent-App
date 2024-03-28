FROM python:3.12 AS base


# Install dependencies
RUN apt-get update && apt-get install build-essential graphviz graphviz-dev --assume-yes
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install psycopg2-binary
RUN pip install whitenoise

# Adding code
WORKDIR /BookForRent
ADD . .
COPY . .
RUN ["chmod", "+x", "BookForRent/docker_entrypoint.sh"]

# ---- Nginx ----
FROM nginx:1.19.0-alpine AS nginx
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

# ---- Release ----
FROM base AS release
COPY --from=nginx /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf
CMD ["nginx", "-g", "daemon off;"]

EXPOSE 8000
ENTRYPOINT ["BookForRent/docker_entrypoint.sh"]
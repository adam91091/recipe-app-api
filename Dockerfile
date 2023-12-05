FROM python:3.9-alpine3.13
LABEL maintainer="adam91091"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
# Docker helper scripts location
COPY ./scripts /scripts
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
# linux-headers is requirement for USGI server installation
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    # create directories for media and static as the user.
    # otherwise, django app would not be able to access the data
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    # change owner of /vol directory and all subdirs to django-user
    chown -R django-user:django-user /vol && \
    # change permission of entire dir - django-user can make any changes
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"
# Only for VSC purpose - not applicable for production!!!
# RUN mkdir -p /home/django-user && \
#     chmod -R 777 /home/django-user

# RUN mkdir -p /tmp && \
#     chmod -R 777 /tmp

USER django-user

CMD ["run.sh"]

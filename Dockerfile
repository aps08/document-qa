FROM python:3.12-slim

ARG DOCKER_GROUP=docteam
ARG DOCKER_USER=docUser

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN groupadd -g 1234 $DOCKER_GROUP && \
    useradd -m -u 1234 -g $DOCKER_GROUP $DOCKER_USER

WORKDIR /app/$DOCKER_USER

COPY start.sh .

RUN chmod +x start.sh

RUN chown -R $DOCKER_USER:$DOCKER_GROUP /app/$DOCKER_USER

USER $DOCKER_USER

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

COPY --chown=$DOCKER_USER:$DOCKER_GROUP . .

EXPOSE 8000

CMD ["./start.sh"]
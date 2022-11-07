FROM python:3.9
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR bots

COPY .. .
RUN pip install -r bot/requirements.txt
ENV PYTHONPATH="$PYTHONPATH:/bots"
EXPOSE 5000
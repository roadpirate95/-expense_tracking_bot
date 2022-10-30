# Pull base image
FROM python:3.9

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory


# Install dependencies
WORKDIR bots

COPY .. .
RUN pip install -r bot/requirements.txt
ENV PYTHONPATH="$PYTHONPATH:/bots"
EXPOSE 5000
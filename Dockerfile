# Use Debian stable as base image
FROM debian:stable

# Set working directory
WORKDIR /app

# Copy everything into /app
COPY . /app

# Install Python3 and Pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv

RUN python3 -m venv .venv
# Activate virtual environment
SHELL ["/bin/bash", "-c"]
RUN source /app/.venv/bin/activate

# Install dependencies using pip
RUN /app/.venv/bin/pip install -r /app/requirements.txt


# Add cronjob
RUN apt-get install -y cron
RUN echo "*/50 * * * * cd /app && /app/.venv/bin/python ./get-recently-played.py >> /var/log/cron.log 2>&1" >> /etc/crontab
RUN echo "*/60 * * * * cd /app && /app/.venv/bin/python ./extract-recently-played.py >> /var/log/cron.log 2>&1" >> /etc/crontab
RUN crontab /etc/crontab
RUN touch /var/log/cron.log

# Run cron on container startup
CMD cron && tail -f /var/log/cron.log
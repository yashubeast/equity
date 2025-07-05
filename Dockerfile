FROM python:3.11-slim

# set working directory
WORKDIR /opt/equity

# install git and other dependencies
RUN apt-get update && \
	apt-get install -y git && \
	apt-get clean

# clone the repo
RUN git clone https://github.com/yashubeast/equity.git .

# create python virtual environment
RUN python -m venv .venv && \
	.venv/bin/pip install --no-cache-dir -r requirements.txt

# create non-root user and group
# RUN addgroup --system equity && \
# 	adduser --system --ingroup equity --home /opt/equity equity

# change ownership
# RUN chown -R equity:equity /opt/equity

# switch to non-root user
# USER equity

# set virtual environment
ENV PATH="/opt/equity/.venv/bin:$PATH"

# disable output buffering
ENV PYTHONUNBUFFERED=1

# run the bot
CMD ["python", "Bot.py"]

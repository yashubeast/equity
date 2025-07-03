# ==============================build stage==============================
FROM python:3.11-slim AS builder

WORKDIR /build

# install git and other dependencies
RUN apt-get update && \
	apt-get install -y git && \
	apt-get clean

# clone the repository
RUN git clone https://github.com/yashubeast/equity.git .

# create python virtual environment
RUN python -m venv .venv && \
	.venv/bin/pip install --no-cache-dir -r req.txt

# ==============================final stage==============================
FROM python:3.11-slim

# install git and other dependencies
RUN apt-get update && \
	apt-get install -y git && \
	apt-get clean

# create non-root user and group
RUN addgroup --system equity && \
	adduser --system --ingroup equity --home /opt/equity equity

# set working directory
WORKDIR /opt/equity

# copy the installed packages from the builder stage
COPY --from=builder /build /opt/equity

# change ownership
RUN chown -R equity:equity /opt/equity && \
	chmod +x run.sh

# switch to non-root user
USER equity

# set virtual environment
ENV PATH="/opt/equity/.venv/bin:$PATH"

# run the bot
CMD ["python", "Bot.py"]


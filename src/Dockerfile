FROM python:3.10-slim

# Set dir and user
ENV GROUP_NAME=app
ENV HOME=/app
ENV GROUP_ID=11000
ENV USER_ID=11001
ENV PORT=8080

# Add user
RUN addgroup --gid $GROUP_ID $GROUP_NAME && \
    adduser $USER_ID -u $USER_ID -D -G $GROUP_NAME -h $HOME

# Install packages
# RUN apt-get update && apt-get install -y build-essential

# Copy files and set working dir
COPY . $HOME
WORKDIR $HOME

# Install python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Open port
EXPOSE $PORT

# Set user
USER $USER_ID

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port", "8080"]
# Use the official Python image from the Docker Hub
# FROM python:3.10-slim
FROM python

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file
COPY etc/requirements.txt .

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Run the Python script
# CMD ["python", "game_process_calculator/main.py"]
# CMD ["python", "crud_sqlmodel.py"]


# FROM python:3

# # Container
# RUN pip install --upgrade pip

# # Environment
# WORKDIR /usr/src

# RUN mkdir -p /usr/src/etc
# COPY etc/ /usr/src/etc/
# RUN pip install --no-cache-dir -r etc/requirements.txt


# RUN mkdir -p /usr/src/game_process_calculator
# COPY game_process_calculator/ /usr/src/game_process_calculator/
# # COPY etc/entrypoint.sh /usr/src/etc/entrypoint.sh
# # RUN chmod 777 ./etc/entrypoint.sh

# # Container

# # COPY . /usr/src
# # RUN chmod 777 ./etc/entrypoint.sh

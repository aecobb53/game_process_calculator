FROM python:3

# Container
RUN pip install --upgrade pip

# Environment
WORKDIR /usr/src
RUN echo 'its been updated'

RUN mkdir -p /usr/src/etc
COPY etc/ /usr/src/etc/
RUN pip install --no-cache-dir -r etc/requirements.txt


RUN mkdir -p /usr/src/game_process_calculator
COPY game_process_calculator/ /usr/src/game_process_calculator/
# COPY etc/entrypoint.sh /usr/src/etc/entrypoint.sh
# RUN chmod 777 ./etc/entrypoint.sh

# Container

# COPY . /usr/src
# RUN chmod 777 ./etc/entrypoint.sh

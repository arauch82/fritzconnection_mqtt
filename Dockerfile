FROM python:3

WORKDIR /usr/src/app

COPY fritzconnection_mqtt.py ./
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Define default command
ENTRYPOINT ["python", "./fritzconnection_mqtt.py"]
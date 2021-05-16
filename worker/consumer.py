import os
import json
from os.path import join, dirname
from dotenv import load_dotenv
import pika
import cv2
import numpy as np
import base64

from PIL import Image
import io

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

AMQP_URL = os.environ.get("AMQP_URL")

params = pika.URLParameters(AMQP_URL)

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='worker')

def stringToRGB(base64_string):
    imgdata = base64.b64decode(str(base64_string))
    image = Image.open(io.BytesIO(imgdata))
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

def callback(ch, method, properties, body):
    print('Received in worker')
    data = json.loads(body)
    img = stringToRGB(data['msg']['file'])
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.imwrite(f'images/{data["msg"]["id"]}.jpg', img)

channel.basic_consume(queue='worker', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
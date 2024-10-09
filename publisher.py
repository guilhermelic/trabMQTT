import base64
from library.lib import tirar_foto
from cryptography.fernet import Fernet
from datetime import datetime
import paho.mqtt.client as mqtt
import json

# Carrega a chave de criptografia
with open("secret.key", "rb") as key_file:
    key = key_file.read()

cipher = Fernet(key)

# Executado ao conectar no broker
def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao broker MQTT com código: {rc}")
    
def publicar_imagem():
    hour = datetime.now()
    
    if tirar_foto():
        with open("./publisherData/image.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    else:
        print("Erro ao tirar a imagem")
        return

    # Criptografa a imagem
    encrypted_image = cipher.encrypt(encoded_string.encode())

    # Formata os dados para o envio
    data = {
        "image": encrypted_image.decode('utf-8'),
        "hour": hour.strftime("%Y-%m-%d %H:%M:%S.%f")
    }

    # Publica os dados no tópico MQTT
    client.publish("camera/imagem", json.dumps(data))
    print("Imagem publicada com sucesso!")

# Configura o cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect

# Conectar ao broker MQTT
client.connect("localhost", 1883, 60)

# Inicia o loop MQTT em segundo plano
client.loop_start()

# Publica a imagem
publicar_imagem()
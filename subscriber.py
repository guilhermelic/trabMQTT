import base64
from datetime import datetime
from cryptography.fernet import Fernet
import paho.mqtt.client as mqtt
import json

# Carrega a chave de criptografia
with open("secret.key", "rb") as key_file:
    key = key_file.read()

cipher = Fernet(key)

# Executado ao conectar no broker
def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao broker MQTT com código: {rc}")
    client.subscribe("camera/imagem")  # Assina o tópico

# Executado quando mensagem for recebida
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode('utf-8'))

        # Descriptografa a imagem
        encrypted_image = data["image"].encode()
        decrypted_image = cipher.decrypt(encrypted_image).decode('utf-8')

        # Decodifica a imagem de base64
        decoded_image = base64.b64decode(decrypted_image)

        # Salva a imagem no disco com timestamp
        hour_now = datetime.now()
        with open(f"./subscriberData/image{hour_now.strftime('%Y%m%d_%H%M%S')}.png", "wb") as image_file:
            image_file.write(decoded_image)

        request_hour = datetime.strptime(data["hour"], "%Y-%m-%d %H:%M:%S.%f")
        print(f"Imagem recebida e salva com sucesso. Tempo de transmissão: {hour_now - request_hour}")
    
    except Exception as e:
        print(f"Erro ao processar a mensagem: {str(e)}")

# Configura o cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Conectar com o broker em localhost, porta 1883
client.connect("localhost", 1883, 60)

# Inicia o loop MQTT
client.loop_forever()
# Aplicação de Envio de Imagem Criptografada

Essa aplicação utiliza o protocolo de comunicação MQTT para capturar imagens no arquivo publisher.py, que publica as imagens para serem recebidas pelo arquivo subscriber.py.

Obs: para rodar o código de maneira correta, precisa-se estar dentro do diretório .\trabMQTT.

## Funcionamento

- Roda-se um broker local MQTT (Fizemos usando mosquitto, usando o comando "mosquitto -v" rodando na porta 1883).
- O subscriber se inscreve no tópico chamado "camera/imagem".
- O usuário publica a imagem criptografada no tópico chamado "camera/imagem".
- O subscriber recebe a imagem criptografada, descriptografa e armazena em subscriberData.

### Criptografia

Para a criptografia foi utilizada a biblioteca Fernet, contendo uma secret key em secret.key.

### Imagem

Para capturar a foto da câmera foi utilizada a biblioteca OpenCV.

## Respostas

### 1. Quem vai ser o ‘servidor’ que recebe as fotos?

Nesse caso, o subscriber. Porém, não há um servidor tradicional como no protocolo HTTP, ao invés disso, o broker age como intermediário na comunicação e entrega os dados para todos os subscribers do tópico “camera/imagem”, que nesse trabalho é a foto, e armazena-a.

### 2. Como o cliente é ‘demandado’ a enviar a foto?

Uma das formas que poderia ser implementada, seria fazer um novo tópico para que o publicador da imagem que fizemos fosse subscriber, e quando recebesse essa mensagem publicasse a foto.
Porém, fizemos o publisher publicar essa mensagem sempre que executar o código publisher.py.

### 3. Como garantir a confidencialidade da foto com MQTT?

Como abordado no tópico Funcionamento/Criptografia, foi utilizada uma chave secreta, onde publisher e subscriber tinham acesso.

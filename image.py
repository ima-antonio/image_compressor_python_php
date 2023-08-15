from flask import Flask, request, jsonify
from PIL import Image
import base64
import io

app = Flask(__name__)

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        # Receber a imagem em base64 da requisição
        data = request.json['image']
        image_data = base64.b64decode(data)

        # Abrir a imagem usando o Pillow
        image = Image.open(io.BytesIO(image_data))

        # Definir as dimensões desejadas
        new_width = 600
        new_height = 800

        # Redimensionar a imagem
        resized_image = image.resize((new_width, new_height))

        # Comprimir a imagem e ajustar a qualidade
        compressed_image = io.BytesIO()
        resized_image.save(compressed_image, format='JPEG', quality=85)
        compressed_image.seek(0)

        # Codificar a nova imagem em base64
        new_image_base64 = base64.b64encode(compressed_image.read()).decode()

        return jsonify({'new_image': new_image_base64})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

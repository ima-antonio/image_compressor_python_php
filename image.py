from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont
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

        # Converter a imagem para o modo RGB se estiver no modo RGBA
        if image.mode == 'RGBA':
            image = image.convert('RGB')

        # Definir a largura desejada e calcular a altura correspondente
        new_width = 700
        aspect_ratio = image.width / image.height
        new_height = int(new_width / aspect_ratio)

        # Redimensionar a imagem para a nova largura e altura calculada
        resized_image = image.resize((new_width, new_height))

        # Definir a altura de corte
        target_height = 850

        # Cortar a imagem para manter a largura e ajustar a altura
        if resized_image.height > target_height:
            upper = (resized_image.height - target_height) // 2
            lower = upper + target_height
            cropped_image = resized_image.crop((0, upper, new_width, lower))
        else:
            cropped_image = resized_image

        # Comprimir a imagem e ajustar a qualidade
        compressed_image = io.BytesIO()
        cropped_image.save(compressed_image, format='JPEG', quality=85)
        compressed_image.seek(0)

        # Adicionar o texto à imagem
        draw = ImageDraw.Draw(cropped_image)
        font = ImageFont.load_default()
        text = "xyz"
        draw.text((10, cropped_image.height - 20), text, fill='white', font=font)

        # Codificar a nova imagem em base64
        new_image_base64 = base64.b64encode(compressed_image.read()).decode()

        return jsonify({'img': new_image_base64})

    except Exception as e:
        return jsonify({'erro': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

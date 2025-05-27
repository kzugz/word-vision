from flask import Flask, request, jsonify
from flask_cors import CORS
from ocr import extract_text_from_image

app = Flask(__name__)
CORS(app)  # libera o frontend para consumir a API

@app.route('/ocr', methods=['POST'])
def ocr_route():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    try:
        image_file = request.files['image']
        image_bytes = image_file.read()
        palavra = extract_text_from_image(image_bytes)
        return jsonify({'palavra_detectada': palavra})
    except Exception as e:
        # Captura qualquer erro que ocorrer e retorna um JSON com a mensagem do erro
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
import random
import barcode
from barcode.writer import ImageWriter
from flask import Flask, render_template_string, request, redirect, url_for
import os

app = Flask(__name__)

# Ensure static directory exists
os.makedirs('static', exist_ok=True)

def generate_random_id():
    prefixes = ['3010', '3011', '3012']
    prefix = random.choice(prefixes)
    suffix = str(random.randint(0, 9999)).zfill(4)
    return prefix + suffix

def generate_barcode(id_number):
    code39 = barcode.Code39(id_number, writer=ImageWriter(), add_checksum=False)
    filename = code39.save(f'static/barcode_{id_number}')
    return f'static/barcode_{id_number}.png'

@app.route('/', methods=['GET', 'POST'])
def index():
    barcodes = []
    if request.method == 'POST':
        random_ids = [generate_random_id() for _ in range(10)]
        barcodes = [(rid, generate_barcode(rid)) for rid in random_ids]
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Random ID Generator</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            h1 { margin-bottom: 20px; }
            .container { max-width: 600px; margin: 0 auto; }
            .barcode { margin-bottom: 20px; }
            button { padding: 10px 20px; font-size: 16px; cursor: pointer; }
        </style>
    </head>
    <body>
        <h1>Random ID Generator</h1>
        <form method="POST">
            <button type="submit">Generate IDs and Barcodes</button>
        </form>
        <div class="container">
            {% for rid, barcode in barcodes %}
                <div class="barcode">
                    <p>ID: {{ rid }}</p>
                    <img src="{{ barcode }}" alt="Barcode for {{ rid }}">
                </div>
            {% endfor %}
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, barcodes=barcodes)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

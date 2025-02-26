import random
import barcode
from barcode.writer import ImageWriter
from flask import Flask, render_template_string

app = Flask(__name__)

def generate_random_id():
    prefixes = ['3010', '3011', '3012']
    prefix = random.choice(prefixes)
    suffix = str(random.randint(0, 9999)).zfill(4)
    return prefix + suffix

def generate_barcode(id_number):
    code39 = barcode.get('code39', id_number, writer=ImageWriter())
    filename = code39.save(f'static/barcode_{id_number}')
    return f'static/barcode_{id_number}.png'

@app.route('/')
def index():
    random_ids = [generate_random_id() for _ in range(10)]
    barcodes = [(rid, generate_barcode(rid)) for rid in random_ids]
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Random ID Generator</title>
    </head>
    <body>
        <h1>Generated IDs and Barcodes</h1>
        <ul>
            {% for rid, barcode in barcodes %}
                <li>{{ rid }}<br><img src="{{ barcode }}" alt="Barcode for {{ rid }}"></li>
            {% endfor %}
        </ul>
    </body>
    </html>
    '''
    return render_template_string(html, barcodes=barcodes)

if __name__ == '__main__':
    app.run(debug=True)

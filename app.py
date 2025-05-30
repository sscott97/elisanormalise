from flask import Flask, render_template, request
import numpy as np
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    normalized_data = ''
    if request.method == 'POST':
        raw_data = request.form['data']
        try:
            rows = [line.strip().split() for line in raw_data.strip().split('\n')]
            matrix = np.array(rows, dtype=float)

            pos_controls = matrix[0:2, 0]  # A1 and B1
            mean_pos = np.mean(pos_controls)
            norm_matrix = matrix / mean_pos

            normalized_data = '\n'.join(['\t'.join(f'{val:.3f}' for val in row) for row in norm_matrix])
        except Exception as e:
            normalized_data = f'Error: {e}'

    return render_template('index.html', normalized=normalized_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Render's port
    app.run(host='0.0.0.0', port=port)
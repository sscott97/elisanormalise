from flask import Flask, render_template, request
import numpy as np
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    normalized_result = None
    error = None

    if request.method == 'POST':
        try:
            raw_data = request.form['raw_data']
            rows = raw_data.strip().split('\n')
            matrix = []

            for row in rows:
                values = [float(x.strip()) for x in row.strip().split()]
                matrix.append(values)

            data = np.array(matrix)

            if data.shape != (8, 12):
                raise ValueError("Input must be 8 rows by 12 columns")

            # Use the average of the first two cells in column 1 (A1, B1)
            pos_ctrl_mean = np.mean([data[0][0], data[1][0]])

            normalized = data / pos_ctrl_mean

            # Format the output for pasting into Excel (tab-separated)
            normalized_result = "\n".join(
                ["\t".join(f"{val:.3f}" for val in row) for row in normalized]
            )

        except Exception as e:
            error = str(e)

    return render_template("index.html", result=normalized_result, error=error)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

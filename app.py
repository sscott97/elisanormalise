from flask import Flask, render_template, request
import numpy as np
import os
import math

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
            for i in range(8):  # Always 8 rows
                if i < len(rows):
                    values = rows[i].strip().split()
                else:
                    values = []

                row_values = []
                for j in range(12):  # Always 12 columns
                    if j < len(values):
                        try:
                            val = float(values[j])
                        except ValueError:
                            val = None  # Non-numeric treated as blank
                        row_values.append(val)
                    else:
                        row_values.append(None)  # Missing cell

                matrix.append(row_values)

            data = np.array(matrix, dtype=float)

            # Extract positive controls (first two cells in first column)
            pos_ctrl_vals = [v for v in [data[0,0], data[1,0]] if not math.isnan(v)]
            if len(pos_ctrl_vals) < 2:
                raise ValueError("Positive controls (first two cells in first column) must be numeric")

            pos_ctrl_mean = sum(pos_ctrl_vals) / len(pos_ctrl_vals)

            # Normalize numeric cells, keep blanks as empty strings
            normalized = []
            for row in data:
                norm_row = []
                for val in row:
                    if math.isnan(val):
                        norm_row.append("")
                    else:
                        norm_row.append(f"{val / pos_ctrl_mean:.3f}")
                normalized.append(norm_row)

            # Format output for Excel: tab separated
            normalized_result = "\n".join(["\t".join(row) for row in normalized])

        except Exception as e:
            error = str(e)

    return render_template("index.html", result=normalized_result, error=error)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

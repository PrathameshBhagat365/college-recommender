from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/recommend', methods=['GET'])
def recommend():
    percentile = float(request.args.get('percentile'))
    branch = request.args.get('branch')
    seat_type = request.args.get('seat_type')

    df = pd.read_csv('colleges.csv')

    filtered = df[
        (df['branch'] == branch) &
        (df['seat_type'] == seat_type) &
        (df['cutoff'] >= percentile - 5) &
        (df['cutoff'] <= percentile + 5)
    ]

    filtered['difference'] = abs(filtered['cutoff'] - percentile)
    result = filtered.sort_values('difference').head(10)

    return jsonify(result[['college_name', 'branch', 'seat_type', 'cutoff']].to_dict(orient='records'))

app.run(host='0.0.0.0', port=81)

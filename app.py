from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

log_data_path = '/Users/bishalkhatiwada/Desktop/6th sem/Server Log Analyzer/access.csv'
log_df = pd.read_csv(log_data_path)


def get_chart_data(selected_category):
    if selected_category == 'IP':
        # Group by 'Country' and count unique IPs
        chart_data = log_df.groupby('Country')['IP'].nunique().to_dict()
    else:
        chart_data = log_df[selected_category].value_counts().to_dict()
    return chart_data


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/chart_data/<selected_category>')
def fetch_chart_data(selected_category):
    data = get_chart_data(selected_category)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
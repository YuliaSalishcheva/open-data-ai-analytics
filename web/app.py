from flask import Flask, render_template
import os
import pandas as pd
from sqlalchemy import create_engine
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
db_url = os.getenv('DATABASE_URL', 'postgresql://user:password@db:5432/analytics_db')
engine = create_engine(db_url)
metrics = PrometheusMetrics(app)
@app.route('/')
def index():
    try:
        df = pd.read_sql('SELECT * FROM raw_data LIMIT 15', engine)
        data_html = df.to_html(classes='table table-striped', index=False)
    except Exception as e:
        print(f"Database error: {e}")
        data_html = "Дані в базі поки що відсутні. Перевірте роботу data_load."

    plot_path = '/app/static/plots'
    plots = os.listdir(plot_path) if os.path.exists(plot_path) else []
    plots = [p for p in plots if p.endswith(('.png', '.jpg', '.jpeg'))]

    return render_template('index.html', data_table=data_html, plots=plots)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
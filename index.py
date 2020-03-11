from flask import Flask, escape, jsonify, send_file
from flask_cors import CORS, cross_origin
from datetime import datetime, timedelta
from tceq import API

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Initialize sites
api = API()


@app.route('/api/sites')
@cross_origin()
def api_sites():
    return api.get_sites()


@app.route('/api/sites/<site_id>')
@cross_origin()
def api_site_data(site_id):
    d = datetime.today() - timedelta(days=1)
    ts = d.timestamp()
    return api.get_site_data(site_id=site_id, timestamp=ts)


if __name__ == '__main__':
    app.run()

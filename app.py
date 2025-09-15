from flask import Flask, request, jsonify, Response
from functools import wraps
import os
import logging

app = Flask(__name__)
app.config['knowledge_base'] = './knowledge_base'

USERNAME = 'howie-guide'
PASSWORD = 'SushmitaHowie@123'

def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

def authenticate():
    return Response('Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

logging.basicConfig(filename='howie_gpt.log', level=logging.INFO)

@app.route('/materials/<filename>', methods=['GET'])
@requires_auth
def get_material(filename):
    filepath = os.path.join(app.config['MATERIALS_FOLDER'], filename)
    if not os.path.isfile(filepath):
        return jsonify({'error': 'File not found'}), 404

    logging.info(f"Material requested: {filename}")
    return Response(open(filepath, 'rb'), mimetype='application/pdf')

@app.route('/query', methods=['POST'])
@requires_auth
def query():
    data = request.json
    query_text = data.get('query', '')
    logging.info(f"Received query: {query_text}")
    response_text = f"Processed query: {query_text}"
    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

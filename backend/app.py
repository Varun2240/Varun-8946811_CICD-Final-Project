from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/health-check', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Application is running'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

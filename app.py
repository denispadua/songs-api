from flask import Flask, jsonify

from api.views import api_bp

app = Flask(__name__)


@app.errorhandler(404)
def artist_not_found(message):
    return jsonify({'error': message.description, 'status': message.code}), message.code


app.register_blueprint(api_bp)


app.run(debug=True)

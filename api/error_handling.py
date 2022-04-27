from flask import jsonify


def register_error_handling(app):

    @app.errorhandler(400)
    def bad_request(message):
        return jsonify({'error': message.description, 'status': message.code}), message.code

    @app.errorhandler(404)
    def data_not_found(message):
        return jsonify({'error': message.description, 'status': message.code}), message.code

    @app.errorhandler(500)
    def internal_error(message):
        return jsonify({'error': message.description, 'status': message.code}), message.code

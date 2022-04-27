from flask import Flask, redirect

from api.views import api_bp
from api.error_handling import register_error_handling

app = Flask(__name__)


app.register_blueprint(api_bp)


register_error_handling(app)


@app.get('/')
def redirect_to_api():
    return redirect('/api/')


app.run()

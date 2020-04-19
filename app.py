from flask import Flask
from flask_cors import CORS
from routes import blueprint

app = Flask(__name__, static_folder='app/static')
CORS(app)
app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key_for_recipes_sessions'
    app.run(debug=True, host="0.0.0.0", port=5000)

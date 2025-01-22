from flask import Flask
from web.routes.game_routes import game_blueprint
from flask_jwt_extended import JWTManager
from web.routes.user_routes import user_blueprint
from datasource.database import init_db
from container import Container
from config import settings


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY
jwt = JWTManager(app)

init_db(app)

container = Container()
app.config["container"] = container

app.register_blueprint(game_blueprint)
app.register_blueprint(user_blueprint)

if __name__ == "__main__":
    app.run(debug=True)

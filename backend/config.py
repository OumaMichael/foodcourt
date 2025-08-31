import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# Database configuration (Postgres on Render, fallback to SQLite locally)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///app.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT configuration
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "supersecret")
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

app.json.compact = False

# CORS: allow local dev + hosted frontend
CORS(
    app,
    resources={r"/*": {"origins": [
        "http://localhost:3000",
        "https://next-gen-foodcourt-tj7z.vercel.app"
    ]}},
    supports_credentials=True
)

# Naming convention for migrations
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db)
db.init_app(app)

bcrypt = Bcrypt(app)
api = Api(app)
jwt = JWTManager(app)
jwt_blacklist = set()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in jwt_blacklist

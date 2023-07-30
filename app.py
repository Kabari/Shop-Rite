import os
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from config import config_dict
from db import db
from blocklist import BLOCKLIST
from resources.store import blp as store_blp
from resources.item import blp as item_blp
from resources.user import blp as user_blp
from datetime import timedelta

def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    api = Api(app)

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload['jti'] in BLOCKLIST
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({
                "description": "This token has expired",
                "error": "token_expired"
            }), 401
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({
                "description": "Signature verification failed",
                "error": "invalid_token"
            }), 401
        )
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({
                "desciption": "Request does not contain an access token",
                "error": "authorization_required"
            }), 401
        )

    @app.before_first_request
    def create_tables():
        db.create_all()

    api.register_blueprint(store_blp)
    api.register_blueprint(item_blp)
    api.register_blueprint(user_blp)

    return app




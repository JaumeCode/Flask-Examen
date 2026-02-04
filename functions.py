from flask_jwt_extended import create_access_token

def crear_token(data):
    
    return create_access_token(identity=data)
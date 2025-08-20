from flask import Flask, request, jsonify
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os
import base64
from datetime import datetime
import time
import jwt  # For JWT decoding

app = Flask(__name__)
SESSION = requests.Session()
KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

def log_info(message):
    print(f"[INFO] {message}")

def log_error(message):
    print(f"[ERROR] {message}")

def log_debug(message):
    print(f"[DEBUG] {message}")

def decode_jwt_token(jwt_token):
    """
    Decode JWT token and return the actual payload
    """
    try:
        # Decode without verification (since we typically don't have the secret key)
        decoded_payload = jwt.decode(jwt_token, options={"verify_signature": False})
        
        # Convert timestamp fields to proper date format if they exist
        if 'exp' in decoded_payload:
            exp_date = datetime.fromtimestamp(decoded_payload['exp']).strftime("%Y-%m-%d %H:%M:%S")
        else:
            exp_date = None
            
        if 'lock_region_time' in decoded_payload:
            lock_region_date = datetime.fromtimestamp(decoded_payload['lock_region_time']).strftime("%Y-%m-%d %H:%M:%S")
        else:
            lock_region_date = None
        
        # Return the actual decoded payload
        return {
            "account_id": decoded_payload.get("account_id"),
            "nickname": decoded_payload.get("nickname"),
            "noti_region": decoded_payload.get("noti_region"),
            "lock_region": decoded_payload.get("lock_region"),
            "external_id": decoded_payload.get("external_id"),
            "external_type": decoded_payload.get("external_type"),
            "plat_id": decoded_payload.get("plat_id"),
            "client_version": decoded_payload.get("client_version"),
            "emulator_score": decoded_payload.get("emulator_score"),
            "is_emulator": decoded_payload.get("is_emulator"),
            "country_code": decoded_payload.get("country_code"),
            "external_uid": decoded_payload.get("external_uid"),
            "reg_avatar": decoded_payload.get("reg_avatar"),
            "source": decoded_payload.get("source"),
            "lock_region_time": decoded_payload.get("lock_region_time"),
            "client_type": decoded_payload.get("client_type"),
            "signature_md5": decoded_payload.get("signature_md5"),
            "using_version": decoded_payload.get("using_version"),
            "release_channel": decoded_payload.get("release_channel"),
            "release_version": decoded_payload.get("release_version"),
            "exp": decoded_payload.get("exp"),
            "exp_date": exp_date,
            "lock_region_date": lock_region_date
        }
    except jwt.InvalidTokenError as e:
        log_error(f"Invalid JWT token: {e}")
        return None
    except Exception as e:
        log_error(f"Error decoding JWT: {e}")
        return None

@app.route("/decode_jwt", methods=["GET"])
def decode_jwt():
    """
    Decode a JWT token and return its payload
    """
    jwt_token = request.args.get("jwt_token")
    
    if not jwt_token:
        return jsonify({
            "success": False,
            "message": "Missing jwt_token parameter"
        }), 400
    
    decoded_data = decode_jwt_token(jwt_token)
    
    if not decoded_data:
        return jsonify({
            "success": False,
            "message": "Failed to decode JWT token"
        }), 400
    
    return jsonify({
        "success": True,
        "data": decoded_data
    })

@app.route("/api/get_jwt", methods=["GET"])
def get_jwt():
    # ... (keep your existing get_jwt function as is) ...
    # This is just a placeholder to show where your existing code would go
    return jsonify({"message": "This is your existing get_jwt endpoint"})

@app.errorhandler(404)
def not_found(error):
    return jsonify({"detail": "Not Found"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    log_info(f"Iniciando o serviço na porta {port}")
    app.run(host="0.0.0.0", port=port)
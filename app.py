import time
import jwt
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/decode', methods=['GET', 'POST'])
def decode_jwt_token():
    try:
        # GET ke case me ?token=... query param se lena
        token = request.args.get("token") if request.method == "GET" else request.json.get("token")
        if not token:
            return jsonify({"error": "Token is required"}), 400

        # Remove "Bearer " if present
        if token.startswith("Bearer "):
            token = token.split(" ", 1)[1]

        import jwt
        decoded = jwt.decode(token, options={"verify_signature": False})

        response_data = {
            "account_id": decoded.get("account_id", 0),
            "nickname": decoded.get("nickname", ""),
            "noti_region": decoded.get("noti_region", ""),
            "lock_region": decoded.get("lock_region", ""),
            "external_id": decoded.get("external_id", ""),
            "external_type": decoded.get("external_type", 0),
            "plat_id": decoded.get("plat_id", 0),
            "client_version": decoded.get("client_version", ""),
            "emulator_score": decoded.get("emulator_score", 0),
            "is_emulator": decoded.get("is_emulator", False),
            "country_code": decoded.get("country_code", ""),
            "external_uid": decoded.get("external_uid", 0),
            "reg_avatar": decoded.get("reg_avatar", 0),
            "source": decoded.get("source", 0),
            "lock_region_time": decoded.get("lock_region_time", 0),
            "client_type": decoded.get("client_type", 0),
            "signature_md5": decoded.get("signature_md5", ""),
            "using_version": decoded.get("using_version", 0),
            "release_channel": decoded.get("release_channel", ""),
            "release_version": decoded.get("release_version", ""),
            "exp": decoded.get("exp", 0),
            "exp_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(decoded.get("exp", 0))) if decoded.get("exp") else "",
            "lock_region_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(decoded.get("lock_region_time", 0))) if decoded.get("lock_region_time") else ""
        }
        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
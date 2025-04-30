from flask import Flask, request, render_template, jsonify
import hashlib
import hmac

app = Flask(__name__)

# Ganti dengan token dari BotFather
BOT_TOKEN = '7831940586:AAGCeVL6eTeEfqmCRnRp4Cwhqzb3rI7qxnM'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auth/telegram', methods=['POST'])
def auth_telegram():
    data = request.json
    if not data:
        return jsonify({"message": "No data received"}), 400

    received_hash = data.pop('hash', '')
    auth_data = "\n".join([f"{k}={data[k]}" for k in sorted(data.keys())])

    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    calculated_hash = hmac.new(secret_key, auth_data.encode(), hashlib.sha256).hexdigest()

    if calculated_hash == received_hash:
        return jsonify({"message": f"Selamat datang, {data.get('first_name', 'User')}!"})
    else:
        return jsonify({"message": "Verifikasi gagal"}), 401

if __name__ == '__main__':
    app.run(debug=True)

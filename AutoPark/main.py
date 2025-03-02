from flask import Flask, request, jsonify, render_template, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Geçici veritabanı (gerçek projede SQLite veya başka bir veritabanı kullanılabilir)
members = []  # Kayıtlı müşteriler
parking_lot = []  # Şu an otoparkta olan araçlar
admin_credentials = {"admin": "password123"}  # Basit admin girişi için
hourly_rate = 10  # Saatlik ücret (varsayılan)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if username in admin_credentials and admin_credentials[username] == password:
        return jsonify({"success": True, "redirect": url_for('admin_panel')})
    return jsonify({"success": False, "message": "Geçersiz kullanıcı adı veya şifre"})

@app.route('/admin')
def admin_panel():
    return render_template('admin.html')

@app.route('/customer')
def customer_panel():
    return render_template('customer.html')

@app.route('/add_member', methods=['POST'])
def add_member():
    data = request.json
    entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_member = {
        "name": data["name"],
        "tc": data["tc"],
        "car_model": data["car_model"],
        "license_plate": data["license_plate"],
        "entry_time": entry_time
    }
    members.append(new_member)
    parking_lot.append(new_member)  # Otoparka ekleniyor
    return jsonify({"message": "Araç başarıyla giriş yaptı."})

@app.route('/set_price', methods=['POST'])
def set_price():
    global hourly_rate
    data = request.json
    hourly_rate = float(data.get("hourly_rate", hourly_rate))
    return jsonify({"message": f"Saatlik ücret {hourly_rate} TL olarak güncellendi."})

@app.route('/current_parking', methods=['GET'])
def current_parking():
    return jsonify(parking_lot)

@app.route('/all_members', methods=['GET'])
def all_members():
    return jsonify(members)

if __name__ == '__main__':
    app.run(debug=True)
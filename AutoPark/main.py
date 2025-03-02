from flask import Flask, request, jsonify, render_template, redirect, url_for
import json
import os

app = Flask(__name__)

# Kullanıcı ve otopark verilerinin saklanacağı JSON dosyaları
DATA_FILE = "users.json"
PARKING_FILE = "parking.json"

def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def save_users(users):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)

def load_parking():
    if os.path.exists(PARKING_FILE):
        with open(PARKING_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def save_parking(parking):
    with open(PARKING_FILE, "w", encoding="utf-8") as file:
        json.dump(parking, file, indent=4)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    users = load_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
            if user.get("is_admin", False):
                return jsonify({"success": True, "redirect": url_for('admin_panel')})
            return jsonify({"success": True, "redirect": url_for('customer_panel')})
    
    return jsonify({"success": False, "message": "Geçersiz kullanıcı adı veya şifre"})

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    name = data.get("name")
    tc = data.get("tc")
    is_admin = data.get("is_admin", False)  # Varsayılan olarak kullanıcı admin değil
    
    users = load_users()
    
    # Kullanıcı adı kontrolü
    if any(user["username"] == username for user in users):
        return jsonify({"success": False, "message": "Bu kullanıcı adı zaten alınmış."})
    
    new_user = {"username": username, "password": password, "name": name, "tc": tc, "is_admin": is_admin}
    users.append(new_user)
    save_users(users)
    
    return jsonify({"success": True, "message": "Kayıt başarılı. Giriş yapabilirsiniz."})

@app.route('/admin')
def admin_panel():
    users = load_users()
    parking_lot = load_parking()
    return render_template('admin.html', users=users, parking_lot=parking_lot)

@app.route('/customer')
def customer_panel():
    return render_template('customer.html')

@app.route('/current_parking')
def current_parking():
    parking_lot = load_parking()
    return jsonify(parking_lot)

@app.route('/all_members')
def all_members():
    users = load_users()
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import json, os, time

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Kullanıcı oturumları için gerekli

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

# Boş yerleri bulan yardımcı fonksiyon
def find_available_spot(parking_data):
    # Otopark 10 katlı olacak ve her katın kapasitesi 20 araba
    max_floors = 10
    max_spots_per_floor = 20
    occupied_spots = {}

    # Mevcut araçların yerlerini bir sözlükte topla
    for car in parking_data:
        floor = car.get("otopark_kati", 1)
        spot = car.get("park_sirasi", 0)
        if floor not in occupied_spots:
            occupied_spots[floor] = set()
        occupied_spots[floor].add(spot)

    # İlk boş yeri bul (1. kattan 10. kata kadar kontrol et)
    for floor in range(1, max_floors + 1):
        if floor not in occupied_spots:
            return {"otopark_kati": floor, "park_sirasi": 1}  # Eğer kat boşsa, 1. sıradan başla
        if len(occupied_spots[floor]) < max_spots_per_floor:  # Kat dolu değilse
            for spot in range(1, max_spots_per_floor + 1):
                if spot not in occupied_spots[floor]:
                    return {"otopark_kati": floor, "park_sirasi": spot}

    # Eğer tüm katlar doluysa (10 kat x 20 araba = 200 araba), None döndür
    return None

@app.route('/')
def home():
    return render_template('login.html')

@app.route("/get_price", methods=["GET"])
def get_price():
    try:
        with open("parking.json", "r") as file:
            parking_data = json.load(file)
        
        # Eğer JSON bir listeyse, ilk elemandan fiyatı alalım
        if isinstance(parking_data, list):
            hourly_rate = parking_data[0].get("hourly_rate", 50)  # Varsayılan 50 TL
        else:
            hourly_rate = parking_data.get("hourly_rate", 50)

        return jsonify({"hourly_rate": hourly_rate})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/set_price", methods=["POST"])
def set_price():
    if "is_admin" not in session or not session["is_admin"]:
        return jsonify({"success": False, "message": "Yetkisiz erişim"}), 403

    data = request.json
    new_price = data.get("hourly_rate")

    if new_price is None or not str(new_price).isdigit():
        return jsonify({"success": False, "message": "Geçerli bir fiyat giriniz"}), 400

    new_price = int(new_price)

    try:
        # JSON dosyasını oku
        with open("parking.json", "r") as file:
            parking_data = json.load(file)

        # Eğer JSON bir listeyse, ilk öğeye saatlik ücreti ekleyelim
        if isinstance(parking_data, list):
            if len(parking_data) > 0 and isinstance(parking_data[0], dict):
                parking_data[0]["hourly_rate"] = new_price
            else:
                return jsonify({"success": False, "message": "Geçersiz JSON formatı"}), 500
        else:
            parking_data["hourly_rate"] = new_price  # JSON bir sözlükse direkt ekleyelim

        # Güncellenmiş veriyi tekrar JSON dosyasına yaz
        with open("parking.json", "w") as file:
            json.dump(parking_data, file, indent=4)

        return jsonify({"success": True, "message": f"Fiyat başarıyla {new_price} TL olarak güncellendi."})

    except Exception as e:
        return jsonify({"success": False, "message": f"Hata oluştu: {str(e)}"}), 500

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    users = load_users()
    
    for user in users:
        if user["username"] == username and user["password"] == password:
            session["username"] = username
            session["name"] = user["name"]
            session["is_admin"] = user.get("is_admin", False)  # Varsayılan olarak False

            if session["is_admin"]:
                return jsonify({"success": True, "redirect": url_for("admin_panel")})
            else:
                # Kullanıcının otopark kaydı var mı kontrol et
                parking_data = load_parking()
                user_parking = next((car for car in parking_data if car["owner"] == user["name"]), None)

                if user_parking:
                    return jsonify({"success": True, "redirect": url_for("parking_info")})  # Park bilgisi sayfasına yönlendir
                
                return jsonify({"success": True, "redirect": url_for("customer_panel")})  # Normal müşteri paneline yönlendir
    
    return jsonify({"success": False, "message": "Invalid credentials"})

@app.route("/logout")
def logout():
    user_name = session.get("name")  # Kullanıcı adını al

    # Kullanıcı park verisini güncelle (sil)
    parking_data = load_parking()
    parking_data = [car for car in parking_data if car["owner"] != user_name]  
    save_parking(parking_data)  # Güncellenmiş veriyi kaydet

    # Kullanıcı oturumunu kapat
    session.pop("username", None)
    session.pop("name", None)
    session.pop("is_admin", None)

    return redirect(url_for("home"))

@app.route("/register_car", methods=["POST"])
def register_car():
    if "username" not in session:
        return jsonify({"success": False, "message": "User not logged in"}), 401
    
    data = request.json
    plate = data.get("plate")
    car_type = data.get("car_type")
    fuel_type = data.get("fuel_type")
    user_name = session.get("name")
    timestamp = time.time()
    
    if not plate or not car_type or not fuel_type:
        return jsonify({"success": False, "message": "Missing data"}), 400
    
    parking_data = load_parking()
    
    # Boş bir yer bul
    available_spot = find_available_spot(parking_data)
    
    # Eğer boş yer yoksa (otopark tamamen doluysa), hata döndür
    if available_spot is None:
        return jsonify({"success": False, "message": "Otopark tamamen dolu! (10 kat x 20 araba kapasite)"}), 400
    
    new_entry = {
        "owner": user_name,
        "plate": plate,
        "car_type": car_type,
        "fuel_type": fuel_type,
        "entry_time": timestamp,
        "park_sirasi": available_spot["park_sirasi"],
        "otopark_kati": available_spot["otopark_kati"]
    }
    
    parking_data.append(new_entry)
    save_parking(parking_data)
    
    return jsonify({"success": True, "message": "Car registered successfully", "redirect": url_for("parking_info")})

@app.route("/parking_info")
def parking_info():
    if "username" not in session:
        return redirect(url_for("home"))
    
    user_name = session.get("name")
    parking_data = load_parking()
    user_parking = next((car for car in parking_data if car["owner"] == user_name), None)
    
    if user_parking:    
        if "entry_time" not in user_parking:
            return jsonify({"message": "Entry time not found for this record."}), 500
        
        return render_template("park_info.html", 
                               plate=user_parking["plate"], 
                               park_sirasi=user_parking.get("park_sirasi", "Bilinmiyor"),
                               otopark_kati=user_parking.get("otopark_kati", "Bilinmiyor"),
                               entry_time=int(user_parking["entry_time"]))  # JavaScript için timestamp tam sayı olmalı
    
    return jsonify({"message": "Kayıt edilmiş araba bulunamadı."})

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
    
    # TC kimlik numarası kontrolü
    if any(user["tc"] == tc for user in users):
        return jsonify({"success": False, "message": "Bu TC kimlik numarası zaten kayıtlı."})
    
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
    current_time = time.time()
    
    # Saatlik ücreti al
    hourly_rate = 50  # Varsayılan
    if parking_lot and isinstance(parking_lot, list) and len(parking_lot) > 0:
        hourly_rate = parking_lot[0].get("hourly_rate", 50)

    # Her araç için ücreti ve geçen süreyi dakika bazlı hesapla
    for car in parking_lot:
        if "entry_time" in car:
            duration_seconds = current_time - car["entry_time"]  # Saniye cinsinden süre
            duration_minutes = int(duration_seconds / 60)  # Dakika cinsine çevir (tam sayı)
            car["duration_minutes"] = duration_minutes  # Geçen süreyi ekle

            # Ücreti hesapla (ilk 30 dakika ücretsiz)
            if duration_minutes <= 30:
                car["fee"] = 0
            else:
                # 30 dakikadan sonrası için ücreti hesapla
                chargeable_minutes = duration_minutes - 30
                # Dakika başına ücreti hesapla (saatlik ücreti 60'a bölerek)
                minute_rate = hourly_rate / 60
                # Ücreti tam sayı olarak yuvarla
                car["fee"] = int(round(chargeable_minutes * minute_rate))
    
    return jsonify(parking_lot)

@app.route('/all_members')
def all_members():
    users = load_users()
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True)
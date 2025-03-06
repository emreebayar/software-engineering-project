# 📌 Otomark - Akıllı Otopark Yönetim Sistemi

Otomark, kullanıcıların otopark durumlarını takip etmelerini sağlayan bir otomasyon sistemidir. Flask ile geliştirilmiş olan bu proje, araç giriş-çıkışlarını kaydederek **otopark katı, park sırası, giriş saati ve ücret hesaplaması** gibi bilgileri kullanıcıya sunar. 🚗💨  

---

## 📂 Proje İçeriği
- **Araç Kaydı:** Kullanıcı, araç bilgilerini girerek otoparka kayıt yapabilir.
- **Otopark Bilgileri:** Kullanıcı, aracının park yeri, kat bilgisi, giriş süresi ve ücret hesaplamasını görebilir.
- **Dinamik Ücretlendirme:** İlk 2 saat ücretsizdir, sonraki her saat başına 50 TL ücret uygulanır.
- **JSON Tabanlı Veri Yönetimi:** Araç bilgileri JSON dosyasında saklanır ve güncellenir.

---

## 🚀 Kurulum

### 1️⃣ Gerekli Bağımlılıkları Yükleyin

Bu projeyi çalıştırmak için aşağıdaki bağımlılıkları yükleyin:

```sh
pip install flask
```

---

### 2️⃣ Projeyi Çalıştırın

Aşağıdaki komutu kullanarak Flask sunucusunu başlatın:

```sh
python main.py
```

Sunucu çalıştığında aşağıdaki URL'den erişebilirsiniz:

```
http://127.0.0.1:5000/
```

---

## 🔗 API Uç Noktaları (Endpoints)

### 📌 Araç Kaydetme (`POST /register_car`)

Bu uç nokta, kullanıcının aracını otoparka kaydetmesini sağlar.

- **İstek (JSON Gövdesi)**:
  ```json
  {
    "plate": "34ABC123",
    "car_type": "Otomobil",
    "fuel_type": "Benzin"
  }
  ```

- **Yanıt (Başarılı)**:
  ```json
  {
    "success": true,
    "message": "Car registered successfully",
    "redirect": "/parking_info"
  }
  ```

---

### 📌 Otopark Bilgisi Getirme (`GET /parking_info`)

Bu uç nokta, kullanıcının otopark durumunu gösterir.

- **Yanıt (Başarılı)**:
  ```json
  {
    "plate": "34ABC123",
    "duration": 1.5,
    "fee": 0,
    "park_sirasi": 5,
    "otopark_kati": 2
  }
  ```

---

## 🎯 Özelleştirme

- Ücretlendirme sistemini değiştirmek için **`parking_info`** fonksiyonundaki ücret hesaplama bölümünü güncelleyebilirsiniz.
- Arayüzü geliştirmek için **`templates/customer.html`** dosyasında değişiklik yapabilirsiniz.

---

## 📌 Katkıda Bulunma

Katkıda bulunmak isterseniz:
1. Bu projeyi `fork` edin. 🍴
2. Yeni bir dal (branch) oluşturun. 🌿  
3. Geliştirme yapıp `commit` edin. 🎯  
4. Pull request gönderin. 🔄  

---

**📜 Lisans:** Bu proje açık kaynak olup MIT Lisansı altında dağıtılmaktadır. 🎉  

🚀 **Kolay gelsin ve iyi kodlamalar!** 🚀

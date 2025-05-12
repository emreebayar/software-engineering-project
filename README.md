# AutoPark - Akıllı Otopark Yönetim Sistemi

**AutoPark**, kullanıcıların otopark durumlarını izlemelerini sağlayan bir otomasyon sistemidir. Flask ile geliştirilmiş bu proje, araç giriş-çıkışlarını kaydederek **otopark katı, park sırası, giriş saati ve ücret hesaplaması** gibi bilgileri sunmaktadır.

---

## Proje İçeriği

- **Araç Kaydı:** Kullanıcılar, araç bilgilerini girerek otoparka kayıt yapabilirler.
- **Otopark Bilgileri:** Kullanıcılar, araçlarının park yeri, kat bilgisi, giriş süresi ve ücret hesaplamalarını görüntüleyebilirler.
- **Dinamik Ücretlendirme:** İlk 2 saat ücretsizdir; sonrasında her saat başına 50 TL ücret uygulanmaktadır.
- **JSON Tabanlı Veri Yönetimi:** Araç bilgileri JSON formatında saklanmakta ve güncellenmektedir.

---

## Kurulum Adımları

### 1. Bağımlılıkların Yüklenmesi

Projeyi çalıştırmadan önce aşağıdaki bağımlılığı yükleyiniz:

```sh
pip install flask
```

---

### 2. Uygulamanın Başlatılması

Flask sunucusunu başlatmak için aşağıdaki komutu çalıştırınız:

```sh
python main.py
```

Başarılı bir şekilde çalıştırıldığında, uygulamaya aşağıdaki URL üzerinden erişebilirsiniz:

```
http://127.0.0.1:5000/
```

---

## API Uç Noktaları

### Araç Kaydı (`POST /register_car`)

Bu uç nokta, kullanıcıların araçlarını otoparka kaydetmelerine olanak tanır.

- **İstek (JSON Gövdesi):**
  ```json
  {
    "plate": "34ABC123",
    "car_type": "Otomobil",
    "fuel_type": "Benzin"
  }
  ```

- **Yanıt (Başarılı Durum):**
  ```json
  {
    "success": true,
    "message": "Car registered successfully",
    "redirect": "/parking_info"
  }
  ```

---

### Otopark Bilgilerini Getirme (`GET /parking_info`)

Bu uç nokta, otoparktaki mevcut durumu ve araç bilgilerini sunar.

- **Yanıt (Başarılı Durum):**
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

## Özelleştirme

- Ücretlendirme sisteminde değişiklik yapmak için **`parking_info`** fonksiyonundaki hesaplama bölümünü düzenleyebilirsiniz.
- Kullanıcı arayüzünde geliştirme yapmak için **`templates/customer.html`** dosyasını özelleştirebilirsiniz.

---

## Katkıda Bulunma

Katkıda bulunmak isteyenler için önerilen adımlar:

1. Bu projeyi `fork`layın.
2. Yeni bir dal (branch) oluşturun.
3. Geliştirmelerinizi yaparak `commit` edin.
4. Pull request gönderin.

---

**Lisans:** Bu proje, MIT Lisansı kapsamında açık kaynak olarak sunulmaktadır.

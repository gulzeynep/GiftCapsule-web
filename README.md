# 🎁 GiftCapsule

Dijital Hediye, Zaman Kapsülü ve MusicJar - Sevdiklerinize özel anılar oluşturun.

## 📋 İçindekiler

- [Özellikler](#özellikler)
- [Teknoloji Stack](#teknoloji-stack)
- [Kurulum](#kurulum)
- [Veritabanı Yapısı](#veritabanı-yapısı)
- [API Endpoints](#api-endpoints)
- [Kullanım](#kullanım)

## ✨ Özellikler

### 🎁 Dijital Hediye
- Sevdiklerinize özel mesajlar ve kartlarla dijital hediye gönderin
- 3 farklı kart teması (Doğum Günü, Aşk, Kutlama)
- Email bildirimleri
- Konfeti animasyonu ile hediye açma deneyimi
- Görüntülenme takibi

### ⏰ Zaman Kapsülü
- Gelecekteki kendinize veya sevdiklerinize mesaj bırakın
- Belirlediğiniz tarihte açılacak kapsüller
- Media URL desteği (fotoğraf, video, ses)
- Hızlı tarih seçimi (1 hafta, 1 ay, 6 ay, 1 yıl)
- Email onayı

### 🎵 MusicJar
- Ruh halinize göre müzik keşfedin
- Dinamik jar tipleri (Mutlu, Hüzünlü, Romantik, Enerjik vb.)
- Rastgele müzik çekme
- YouTube embed player
- Play count takibi
- Kullanıcıların müzik ekleyebilmesi

## 🛠 Teknoloji Stack

### Backend
- **Flask 3.0.0** - Python web framework
- **Supabase** - PostgreSQL database & authentication
- **Flask-CORS** - CORS support
- **Python SMTP** - Email notifications (Gmail)

### Frontend
- **HTML5** - Markup
- **Tailwind CSS** - Styling
- **Vanilla JavaScript** - Interactivity
- **Canvas Confetti** - Konfeti animasyonları

## 🚀 Kurulum

### 1. Projeyi Klonlayın

```bash
git clone https://github.com/yourusername/giftcapsule.git
cd giftcapsule
```

### 2. Backend Kurulumu

```bash
cd backend

# Python sanal ortamı oluşturun (opsiyonel ama önerilir)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# .env dosyası oluşturun
cp .env.example .env
```

### 3. .env Dosyasını Yapılandırın

`.env` dosyasını düzenleyin ve aşağıdaki değerleri doldurun:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
EMAIL_USER=your_gmail@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
```

**Not:** Gmail için App Password oluşturmanız gerekebilir:
1. Google Hesabı > Güvenlik > 2 Adımlı Doğrulama (aktif olmalı)
2. Uygulama Şifreleri > Mail > Şifre oluştur

### 4. Supabase Veritabanını Oluşturun

Supabase projenizde aşağıdaki SQL komutlarını çalıştırın:

```sql
-- Gifts table
CREATE TABLE gifts (
    id SERIAL PRIMARY KEY,
    sender_name TEXT NOT NULL,
    sender_email TEXT NOT NULL,
    recipient_name TEXT NOT NULL,
    recipient_email TEXT NOT NULL,
    occasion TEXT NOT NULL,
    card_template TEXT NOT NULL,
    message TEXT NOT NULL,
    is_viewed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Time Capsules table
CREATE TABLE time_capsules (
    id SERIAL PRIMARY KEY,
    creator_email TEXT NOT NULL,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    media_url TEXT,
    open_date TIMESTAMP NOT NULL,
    is_opened BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Music Jars table
CREATE TABLE music_jars (
    id SERIAL PRIMARY KEY,
    jar_type TEXT NOT NULL,
    song_name TEXT NOT NULL,
    artist_name TEXT NOT NULL,
    youtube_url TEXT NOT NULL,
    added_by TEXT NOT NULL,
    play_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Jar Types table
CREATE TABLE jar_types (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    emoji TEXT NOT NULL,
    description TEXT NOT NULL,
    color TEXT NOT NULL
);

-- Insert default jar types
INSERT INTO jar_types (name, emoji, description, color) VALUES
('Mutlu', '😊', 'Neşeli ve enerjik şarkılar', '#FFD700'),
('Hüzünlü', '😢', 'Duygusal ve hüzünlü melodiler', '#4169E1'),
('Romantik', '💕', 'Aşk dolu romantik şarkılar', '#FF69B4'),
('Enerjik', '⚡', 'Tempolu ve dinamik müzikler', '#FF4500');
```

### 5. Backend Sunucusunu Başlatın

```bash
cd backend
python app.py
```

Backend http://localhost:5000 adresinde çalışacak.

### 6. Frontend'i Başlatın

Frontend statik HTML dosyalarından oluştuğu için basit bir HTTP sunucusu yeterlidir:

```bash
cd frontend

# Python ile
python -m http.server 3000

# veya Node.js ile
npx http-server -p 3000

# veya Live Server (VS Code extension) kullanın
```

Frontend http://localhost:3000 adresinde çalışacak.

## 📊 Veritabanı Yapısı

### gifts
- `id` (SERIAL PRIMARY KEY)
- `sender_name` (TEXT)
- `sender_email` (TEXT)
- `recipient_name` (TEXT)
- `recipient_email` (TEXT)
- `occasion` (TEXT)
- `card_template` (TEXT)
- `message` (TEXT)
- `is_viewed` (BOOLEAN)
- `created_at` (TIMESTAMP)

### time_capsules
- `id` (SERIAL PRIMARY KEY)
- `creator_email` (TEXT)
- `title` (TEXT)
- `message` (TEXT)
- `media_url` (TEXT, nullable)
- `open_date` (TIMESTAMP)
- `is_opened` (BOOLEAN)
- `created_at` (TIMESTAMP)

### music_jars
- `id` (SERIAL PRIMARY KEY)
- `jar_type` (TEXT)
- `song_name` (TEXT)
- `artist_name` (TEXT)
- `youtube_url` (TEXT)
- `added_by` (TEXT)
- `play_count` (INTEGER)
- `created_at` (TIMESTAMP)

### jar_types
- `id` (SERIAL PRIMARY KEY)
- `name` (TEXT, UNIQUE)
- `emoji` (TEXT)
- `description` (TEXT)
- `color` (TEXT)

## 🔌 API Endpoints

### Gifts
- `POST /api/gifts` - Yeni hediye oluştur
- `GET /api/gifts/<id>` - Hediye detaylarını getir
- `PUT /api/gifts/<id>/view` - Hediyeyi görüntülendi olarak işaretle

### Capsules
- `POST /api/capsules` - Yeni zaman kapsülü oluştur
- `GET /api/capsules/<id>` - Kapsül detaylarını getir
- `GET /api/capsules/check/<id>` - Kapsülün açılabilir olup olmadığını kontrol et
- `PUT /api/capsules/<id>/open` - Kapsülü aç

### Music
- `GET /api/music/jars` - Tüm jar tiplerini listele
- `POST /api/music` - Yeni müzik ekle
- `GET /api/music/random/<jar_type>` - Belirli bir jar'dan rastgele müzik getir
- `PUT /api/music/<id>/play` - Play count'u artır

## 📱 Kullanım

### Dijital Hediye Gönderme

1. Ana sayfadan "Hediye Gönder" kartına tıklayın
2. Formu doldurun:
   - Gönderen bilgileri (ad, email)
   - Alıcı bilgileri (ad, email)
   - Özel gün seçin
   - Kart teması seçin
   - Mesajınızı yazın
3. "Hediye Gönder" butonuna tıklayın
4. Alıcı email ile bildirim alacak
5. Share link ile hediyeyi görüntüleyebilirsiniz

### Zaman Kapsülü Oluşturma

1. Ana sayfadan "Kapsül Oluştur" kartına tıklayın
2. Formu doldurun:
   - Email adresiniz
   - Kapsül başlığı
   - Mesajınız
   - Media URL (opsiyonel)
   - Açılış tarihi
3. Hızlı tarih butonlarını kullanabilirsiniz
4. "Zaman Kapsülü Oluştur" butonuna tıklayın
5. Email ile onay alacaksınız

### Müzik Keşfetme

1. Ana sayfadan "Müzik Keşfet" kartına tıklayın
2. Ruh halinize uygun jar'ı seçin
3. Rastgele bir müzik çalacak
4. "Başka Şarkı" ile yeni müzik dinleyin
5. "Müzik Ekle" ile yeni şarkılar ekleyebilirsiniz

## 🎨 Özelleştirme

### Yeni Jar Tipi Ekleme

Supabase'de `jar_types` tablosuna yeni kayıt ekleyin:

```sql
INSERT INTO jar_types (name, emoji, description, color) VALUES
('Nostaljik', '🎸', 'Eski güzel günlerin şarkıları', '#8B4513');
```

### Email Şablonlarını Özelleştirme

`backend/utils/email_sender.py` dosyasındaki HTML şablonlarını düzenleyin.

### Kart Temalarını Özelleştirme

`frontend/view-gift.html` dosyasında yeni gradient renkleri ekleyin:

```css
.card-new-theme {
    background: linear-gradient(135deg, #color1 0%, #color2 100%);
}
```

## 🐛 Bilinen Sorunlar

- Email gönderimi Gmail'in güvenlik ayarlarına bağlı olarak çalışmayabilir (App Password kullanın)
- YouTube embed player bazı videolarda çalışmayabilir (video sahibinin embed izinleri)

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Push edin (`git push origin feature/AmazingFeature`)
5. Pull Request açın

## 📧 İletişim

Sorularınız için: your-email@example.com

---

**GiftCapsule ile sevdiklerinize özel anılar oluşturun!** 🎁
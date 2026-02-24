import sqlite3
import os

def test_veritabani_olusturma():
    print("Jenkins Testi Basliyor...")
    # Jenkins'in veritabanı oluşturma yeteneğini test edelim
    baglanti = sqlite3.connect("test_kutuphane.db")
    im = baglanti.cursor()
    im.execute("CREATE TABLE IF NOT EXISTS kitaplar (id INTEGER PRIMARY KEY, kitap_adi TEXT, yazar TEXT)")
    baglanti.commit()
    baglanti.close()

    # Dosya gerçekten oluştu mu kontrol et
    assert os.path.exists("test_kutuphane.db"), "HATA: Veritabani olusturulamadi!"
    print("Test Basarili: Veritabani sorunsuz olusturuldu ve kodlar calisiyor.")

if __name__ == "__main__":
    test_veritabani_olusturma()
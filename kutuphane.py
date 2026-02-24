import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msgBox
import sqlite3

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kütüphane Yöneticisi")
        self.geometry("400x600")
        self.resizable(width=True, height=True)
        
        # Veritabanını kur
        self.vt_kur()
        
        self.lblName = tk.Label(self, text="DİJİTAL KÜTÜPHANE",
                                fg="black",
                                bg="white",
                                font=("Calibri", 20, "bold"))
        self.lblName.pack(fill=tk.BOTH, pady=30)
        
        btn1 = tk.Button(self, text="Kitap Ekle",
                         command=self.btnEkle,
                         bg="gray", fg="black", font=("Calibri", 20, "bold"))
        btn1.pack(pady=10)
        
        btn2 = tk.Button(self, text="Kitapları Listele",
                         command=self.btnListele,
                         bg="gray", fg="black", font=("Calibri", 20, "bold"))
        btn2.pack(pady=10)
        
        btn3 = tk.Button(self, text="Yazar Sorgula",
                         command=self.btnSorgu,
                         bg="gray", fg="black", font=("Calibri", 20, "bold"))
        btn3.pack(pady=10)
        
        btn4 = tk.Button(self, text="Çıkış",
                         command=self.btnCıkıs,
                         bg="gray", fg="black", font=("Calibri", 20, "bold"))
        btn4.pack(pady=10)

    def vt_kur(self):
        # DÜZELTME: İsim 'kutuphane.db' olarak standartlaştırıldı
        baglanti = sqlite3.connect("kutuphane.db")
        im = baglanti.cursor()
        im.execute("CREATE TABLE IF NOT EXISTS kitaplar (id INTEGER PRIMARY KEY, kitap_adi TEXT, yazar TEXT)")
        baglanti.commit()
        baglanti.close()

    def btnEkle(self):
        yp = tk.Toplevel(self)
        yp.title("Kitap Ekle")
        yp.geometry("300x250")

        tk.Label(yp, text="Kitap Adı:", font=("Calibri", 12, "bold")).pack(pady=5)
        entKi = tk.Entry(yp, font=("Calibri", 12, "bold"))
        entKi.pack(pady=5)

        tk.Label(yp, text="Yazar:", font=("Calibri", 12, "bold")).pack(pady=5)
        entYa = tk.Entry(yp, font=("Calibri", 12, "bold"))
        entYa.pack(pady=5)

        def kaydet():
            ad = entKi.get()
            yazar = entYa.get()
            if ad and yazar:
                # DÜZELTME: İsim 'kutuphane.db' yapıldı
                baglanti = sqlite3.connect("kutuphane.db")
                im = baglanti.cursor()
                im.execute("INSERT INTO kitaplar (kitap_adi, yazar) VALUES (?,?)", (ad, yazar))
                baglanti.commit()
                baglanti.close()
                msgBox.showinfo("Başarılı", "Kitaplar eklendi!")
                yp.destroy()
            else:
                msgBox.showwarning("Hata", "Alanları doldurun!")

        tk.Button(yp, text="KAYDET", command=kaydet, bg="green", fg="white", font=("Calibri", 10, "bold")).pack(pady=20)

    def btnListele(self):
        list_pencere = tk.Toplevel(self)
        list_pencere.title("Kitap Listesi")
        list_pencere.geometry("500x400")

        columns = ("id", "kitap_adi", "yazar")
        tree = ttk.Treeview(list_pencere, columns=columns, show="headings")

        tree.heading("id", text="ID")
        tree.column("id", width=50)
        tree.heading("kitap_adi", text="Kitap Adı")
        tree.heading("yazar", text="Yazar")

        tree.pack(fill=tk.BOTH, expand=True)

        # DÜZELTME: İsim 'kutuphane.db' yapıldı
        baglanti = sqlite3.connect("kutuphane.db")
        im = baglanti.cursor()
        im.execute("SELECT * FROM kitaplar")
        veriler = im.fetchall()
        baglanti.close()

        for veri in veriler:
            tree.insert("", tk.END, values=veri)

    def btnSorgu(self):
        sorgu_pencere = tk.Toplevel(self)
        sorgu_pencere.title("Yazar Sorgula")
        sorgu_pencere.geometry("400x400")

        tk.Label(sorgu_pencere, text="Aradığınız Yazarın Adı:", font=("Calibri", 10)).pack(pady=10)
        entArama = tk.Entry(sorgu_pencere)
        entArama.pack(pady=5)

        # DÜZELTME: 'colums' yazım hatası 'columns' yapıldı
        columns = ("kitap_adi", "yazar")
        tree = ttk.Treeview(sorgu_pencere, columns=columns, show="headings", height=10)
        tree.heading("kitap_adi", text="Kitap Adı")
        tree.heading("yazar", text="Yazar")
        tree.pack(pady=20, fill=tk.BOTH, expand=True)

        def ara():
            aranan = entArama.get()
            for i in tree.get_children():
                tree.delete(i)

            # DÜZELTME: İsim 'kutuphane.db' yapıldı
            baglanti = sqlite3.connect("kutuphane.db")
            im = baglanti.cursor()
            sorgu = "SELECT kitap_adi, yazar FROM kitaplar WHERE yazar LIKE ?"
            im.execute(sorgu, ('%' + aranan + '%',))
            sonuclar = im.fetchall()
            baglanti.close()

            if not sonuclar:
                msgBox.showinfo("Sonuç", "Bu yazara ait kitap bulunamadı.")

            for sonuc in sonuclar:
                tree.insert("", tk.END, values=sonuc)

        tk.Button(sorgu_pencere, text="ARA", command=ara, bg="blue", fg="white").pack(pady=5)

    def btnCıkıs(self):
        self.destroy()

if __name__ == "__main__":
    pencere = Window()
    pencere.mainloop()
import tkinter as tk
from tkinter import ttk
import random

def çanta_optimizasyon(kapasite, eşyalar, num_iterasyonlar, num_işci_arilar, num_gözcü_arilar, num_kasif_arilar, sonuçlar_textbox):
    def çözümü_değerlendir(çözüm):
        toplam_değer = sum(eşyalar[i][0] for i in range(len(çözüm)) if çözüm[i])
        toplam_ağırlık = sum(eşyalar[i][1] for i in range(len(çözüm)) if çözüm[i])
        return toplam_değer, toplam_ağırlık

    def çözüm_üret():
        return [random.randint(0, 1) for _ in range(len(eşyalar))]

    def isci_arilar(çözümler):
        for i in range(num_işci_arilar):
            index = random.randint(0, len(çözümler) - 1)
            aday_çözüm = çözümler[index].copy()
            j = random.randint(0, len(aday_çözüm) - 1)
            k = random.randint(0, len(aday_çözüm) - 1)
            while k == j:
                k = random.randint(0, len(aday_çözüm) - 1)
            aday_çözüm[j] = 1 - aday_çözüm[j]
            if çözümü_değerlendir(aday_çözüm)[1] <= kapasite:
                çözümler[index] = aday_çözüm.copy()

    def gözcü_arilar(çözümler):
        uygunluk_değerleri = [çözümü_değerlendir(çözüm)[0] for çözüm in çözümler]
        toplam_uygunluk = sum(uygunluk_değerleri)
        olasılıklar = [değer / toplam_uygunluk for değer in uygunluk_değerleri]
        for i in range(num_gözcü_arilar):
            seçilen_index = random.choices(range(len(çözümler)), olasılıklar)[0]
            aday_çözüm = çözümler[seçilen_index].copy()
            j = random.randint(0, len(aday_çözüm) - 1)
            k = random.randint(0, len(aday_çözüm) - 1)
            while k == j:
                k = random.randint(0, len(aday_çözüm) - 1)
            aday_çözüm[j] = 1 - aday_çözüm[j]
            if çözümü_değerlendir(aday_çözüm)[1] <= kapasite:
                çözümler[seçilen_index] = aday_çözüm.copy()

    def kasif_arılar_fazı(çözümler):
        for i in range(len(çözümler)):
            if çözümü_değerlendir(çözümler[i])[1] > kapasite:
                çözümler[i] = çözüm_üret()

    # Ana döngü
    çözümler = [çözüm_üret() for _ in range(num_işci_arilar)]
    for iterasyon in range(num_iterasyonlar):
        isci_arilar(çözümler)
        gözcü_arilar(çözümler)
        kasif_arılar_fazı(çözümler)

        # Her iterasyonun sonuçlarını göster
        en_iyi_çözüm = max(çözümler, key=lambda x: çözümü_değerlendir(x)[0])
        en_iyi_değer, en_iyi_ağırlık = çözümü_değerlendir(en_iyi_çözüm)
        sonuçlar_textbox.insert(tk.END, f"Iterasyon {iterasyon+1}: En iyi çözüm: {en_iyi_çözüm}, Toplam değer: {en_iyi_değer}, Toplam ağırlık: {en_iyi_ağırlık}\n")
        sonuçlar_textbox.see(tk.END)  # Scroll to the end of the textbox

    # En iyi çözümü bulma
    en_iyi_çözüm = max(çözümler, key=lambda x: çözümü_değerlendir(x)[0])
    en_iyi_değer, en_iyi_ağırlık = çözümü_değerlendir(en_iyi_çözüm)
    return en_iyi_çözüm, en_iyi_değer, en_iyi_ağırlık

def çantayı_çöz():
    kapasite = int(kapasite_giriş.get())
    eşyalar = [(int(değer_giriş.get()), int(ağırlık_giriş.get())) for değer_giriş, ağırlık_giriş in zip(değer_girişleri, ağırlık_girişleri)]
    num_iterasyonlar = int(iterasyon_giriş.get())
    num_işci_arilar = int(çalışan_arılar_giriş.get())
    num_gözcü_arilar = int(izleyici_arılar_giriş.get())
    num_kasif_arilar = int(keşif_arılar_giriş.get())

    en_iyi_çözüm, en_iyi_değer, en_iyi_ağırlık = çanta_optimizasyon(kapasite, eşyalar, num_iterasyonlar, num_işci_arilar, num_gözcü_arilar, num_kasif_arilar, sonuçlar_textbox)

    sonuç_etiketi.config(text=f"En iyi çözüm: {en_iyi_çözüm}\nToplam değer: {en_iyi_değer}\nToplam ağırlık: {en_iyi_ağırlık}")

def veri_girişi_onayla():
    global veri_sayısı
    veri_sayısı = int(veri_sayısı_giriş.get())
    for widget in pencere.winfo_children():
        widget.destroy()  # Mevcut widget'ları temizle

    oluştur_veri_girişleri()

def oluştur_veri_girişleri():
    global değer_girişleri, ağırlık_girişleri
    değer_girişleri = []
    ağırlık_girişleri = []

    ttk.Label(pencere, text="Lütfen her bir öğenin değerini ve ağırlığını girin:").pack(pady=10)

    for i in range(veri_sayısı):
        frame = ttk.Frame(pencere)
        frame.pack(pady=5)

        ttk.Label(frame, text=f"Öğe {i+1} Değeri (TL):").pack(side=tk.LEFT)
        değer_giriş = ttk.Entry(frame)
        değer_giriş.pack(side=tk.LEFT, padx=5)
        değer_girişleri.append(değer_giriş)

        ttk.Label(frame, text=f"Öğe {i+1} Ağırlığı (kg):").pack(side=tk.LEFT)
        ağırlık_giriş = ttk.Entry(frame)
        ağırlık_giriş.pack(side=tk.LEFT, padx=5)
        ağırlık_girişleri.append(ağırlık_giriş)

    ttk.Label(pencere, text="Optimizasyon Parametreleri").pack()
    ttk.Label(pencere, text="İterasyon Sayısı:").pack()
    global iterasyon_giriş, çalışan_arılar_giriş, izleyici_arılar_giriş, keşif_arılar_giriş, kapasite_giriş, sonuç_etiketi
    iterasyon_giriş = ttk.Entry(pencere)
    iterasyon_giriş.pack()
    ttk.Label(pencere, text="İşçi Arı Sayısı:").pack()
    çalışan_arılar_giriş = ttk.Entry(pencere)
    çalışan_arılar_giriş.pack()
    ttk.Label(pencere, text="İzleyici Arı Sayısı:").pack()
    izleyici_arılar_giriş = ttk.Entry(pencere)
    izleyici_arılar_giriş.pack()
    ttk.Label(pencere, text="Keşif Arı Sayısı:").pack()
    keşif_arılar_giriş = ttk.Entry(pencere)
    keşif_arılar_giriş.pack()

    ttk.Label(pencere, text="Çanta Kapasitesi (kg):").pack()
    kapasite_giriş = ttk.Entry(pencere)
    kapasite_giriş.pack()

    ttk.Button(pencere, text="Optimize Et", command=çantayı_çöz).pack(pady=10)

    global sonuç_etiketi, sonuçlar_textbox
    sonuç_etiketi = ttk.Label(pencere, text="")
    sonuç_etiketi.pack()

    # Sonuçları göstermek için metin kutusu oluştur
    sonuçlar_textbox = tk.Text(pencere, wrap="word", height=15, width=80)
    sonuçlar_textbox.pack()

# Ana pencere
pencere = tk.Tk()
pencere.title("Çanta Problemi Çözücü")

# Veri girişi için giriş alanı
ttk.Label(pencere, text="Kaç adet veri girmek istiyorsunuz?").pack(pady=10)
veri_sayısı_giriş = ttk.Entry(pencere)
veri_sayısı_giriş.pack()
ttk.Button(pencere, text="Devam", command=veri_girişi_onayla).pack(pady=10)

pencere.mainloop()

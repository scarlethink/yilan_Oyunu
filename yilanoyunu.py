import pygame
import random

pygame.init()

# EKRAN BOYUTLARI
genislik = 800
yukseklik = 600

# KULLANILACAK RENKLER
beyaz = (255, 255, 255)
siyah = (0, 0, 0)
pembe = (251, 203, 255)
mavi = (139, 193, 255)
kiraz = (232, 60, 105)
yesil = (0, 255, 0)

dis = pygame.display.set_mode((genislik, yukseklik))  # BELİRTİLEN BOYUTLARDA BİR ALAN OLUŞTURUR
pygame.display.set_caption('Yılan Oyunu')  # PENCERE BAŞLIĞI AYARLAMA

saat = pygame.time.Clock()

yilan_blok = 10  # YILANIN HAREKET EDECEĞİ BLOK SAYISI
yilan_hiz = 15  # YILANIN HAREKET HIZI

font_stil = pygame.font.SysFont(None, 50)
skor_font = pygame.font.SysFont(None, 35)

def mesaj(text, renk, font, y_pos=None):
    metin = font.render(text, True, renk)
    metin_genislik = metin.get_width()
    metin_yukseklik = metin.get_height()
    
    if y_pos is None:
        # Ekranın ortasına yerleştir
        x_pos = (genislik - metin_genislik) / 2
        y_pos = (yukseklik - metin_yukseklik) / 2
    else:
        # Belirtilen y konumuna yerleştir
        x_pos = (genislik - metin_genislik) / 2
    
    dis.blit(metin, [x_pos, y_pos])

# BAŞLANGIÇ EKRANI
def baslangic_ekrani():
    baslangic = True
    while baslangic:
        dis.fill(siyah)
        mesaj("* * * YILAN OYUNU * * *", pembe, font_stil)
        mesaj("Başlamak için herhangi bir tuşa basın", mavi, font_stil, yukseklik / 2 + 50)  # Orta konumdan biraz aşağıda
        pygame.display.update()  # Ekranda yapılan tüm değişiklikleri göstermek için
        
        for event in pygame.event.get():  # pygame.event.get(): Pygame'de oluşan olayları alır. Bu olaylar, kullanıcı girişlerini (fare tıklamaları, klavye basımları, pencere kapama vs.) içerir.
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                baslangic = False

def yilan(yilan_blok, yilan_list):  # Blok kısmı yılanın her bir parçasına tekabül eder, list ise yılanın tüm parçalarına.
    for x in yilan_list:
        pygame.draw.rect(dis, beyaz, [x[0], x[1], yilan_blok, yilan_blok])

def skor(skor):
    deger = skor_font.render("Skor: " + str(skor), True, kiraz)
    dis.blit(deger, [0, 0])

def oyun_dongusu():
    oyun_bitti = False
    oyun_kapandi = False

    # BAŞLANGIÇ KOORDİNATLARI (EKRANIN ORTASINDA OLMASI İÇİN)
    x1 = genislik / 2
    y1 = yukseklik / 2

    # BAŞLANGIÇTA YILANIN HAREKET ETMEMESİ İÇİN HAREKET HIZLARI
    x1_degisiklik = 0
    y1_degisiklik = 0

    # YILANIN UZUNLUĞU BAŞLANGIÇTA YOK. O YÜZDEN DİZİ BOŞ. UZUNLUK YILAN İLE 1 BOYUTUNDA BAŞLAR.
    yilan_list = []
    uzunluk_yilan = 1

    # YEMEK KOMUTLARININ EKRANDA DÜZGÜN BELİRTİLMESİ İÇİN EKRAN GENİŞLİĞİNİ HESABA KATARAK YAZDIK. round KOMUTU İLE DE EN YAKIN TAM SAYIYA YUVARLADIK BOYLECE YEMEKLER EKRANDA DÜZGÜN BELİRDİ.
    yemek_x = round(random.randrange(0, genislik - yilan_blok) / 10.0) * 10.0
    yemek_y = round(random.randrange(0, yukseklik - yilan_blok) / 10.0) * 10.0

    while not oyun_bitti:
        while oyun_kapandi:
            dis.fill(beyaz)
            mesaj("Kaybettin! Tekrar oynamak için Q, çıkmak için C", kiraz, font_stil)
            skor(uzunluk_yilan - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:  # BİR TUŞA BASILDIĞINDA TETİKLENME
                    if event.key == pygame.K_c:  # C TUŞUNA BASILDIĞINDA OYUN BİTER
                        oyun_bitti = True
                        oyun_kapandi = False
                    if event.key == pygame.K_q:  # Q TUŞUYLA YENİDEN BAŞLANIR
                        oyun_dongusu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                oyun_bitti = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if x1_degisiklik == 0:  # Eğer yılan yatay olarak hareket etmiyorsa, sola hareket et
                        x1_degisiklik = -yilan_blok
                        y1_degisiklik = 0
                elif event.key == pygame.K_RIGHT:
                    if x1_degisiklik == 0:  # Eğer yılan yatay olarak hareket etmiyorsa, sağa hareket et
                        x1_degisiklik = yilan_blok
                        y1_degisiklik = 0
                elif event.key == pygame.K_UP:
                    if y1_degisiklik == 0:  # Eğer yılan dikey olarak hareket etmiyorsa, yukarı hareket et
                        y1_degisiklik = -yilan_blok
                        x1_degisiklik = 0
                elif event.key == pygame.K_DOWN:
                    if y1_degisiklik == 0:  # Eğer yılan dikey olarak hareket etmiyorsa, aşağı hareket et
                        y1_degisiklik = yilan_blok
                        x1_degisiklik = 0

        # YILAN EKRAN SINIRLARINA ÇARPTIĞINDA KAYBEDER
        if x1 >= genislik or x1 < 0 or y1 >= yukseklik or y1 < 0:
            oyun_kapandi = True
        
        x1 += x1_degisiklik
        y1 += y1_degisiklik
        
        dis.fill(siyah)
        pygame.draw.rect(dis, yesil, [yemek_x, yemek_y, yilan_blok, yilan_blok])
        
        yilan_bas = [x1, y1]
        yilan_list.append(yilan_bas)
        if len(yilan_list) > uzunluk_yilan:
            del yilan_list[0]

        # YILAN KENDİNE ÇARPTIĞINDA KAYBEDER
        for x in yilan_list[:-1]:
            if x == yilan_bas:
                oyun_kapandi = True

        yilan(yilan_blok, yilan_list)
        skor(uzunluk_yilan - 1)

        pygame.display.update()

        # YILAN YEMEĞİ YEDİĞİNDE
        if x1 == yemek_x and y1 == yemek_y:
            yemek_x = round(random.randrange(0, genislik - yilan_blok) / 10.0) * 10.0
            yemek_y = round(random.randrange(0, yukseklik - yilan_blok) / 10.0) * 10.0
            uzunluk_yilan += 1

        saat.tick(yilan_hiz)  # Yılanın hızını ayarlamak için

    pygame.quit()
    quit()

baslangic_ekrani()
oyun_dongusu()

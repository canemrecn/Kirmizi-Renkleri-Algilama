import cv2
import numpy as np
#cv2 kütüphanesini OpenCV işlevlerine erişmek için içeri aktarıyoruz.
#numpy kütüphanesini sayısal işlemler yapmak için içeri aktarıyoruz.
altRenk = (170, 100, 100)
ustRenk = (190, 255, 255)
RENK = 'KIRMIZI'
#altRenk ve ustRenk, HSV renk uzayında belirlenen bir renk aralığını temsil eder.
#RENK değişkeni, hangi renk üzerinde işlem yapıldığını belirtir.
kamera = cv2.VideoCapture(0)
cember = True
#cv2.VideoCapture(0) ile bir kamera cihazı üzerinden video yakalamayı başlatıyoruz.
#cember değişkeni, konturları çevreleyen bir daire çizilip çizilmeyeceğini belirten bir bayraktır.
while True:
    if not kamera.isOpened():
        break
#Sonsuz bir döngü başlatılır ve döngü içinde video akışının açık olup olmadığı kontrol edilir.
    _,kare = kamera.read()
    hsv = cv2.cvtColor(kare, cv2.COLOR_BGR2HSV)
#kamera.read() ile bir sonraki kareyi yakalayarak _ ve kare değişkenlerine atarız.
#Yakalanan kareyi BGR renk uzayından HSV renk uzayına dönüştürürüz.
    maske = cv2.inRange(hsv,altRenk,ustRenk)
    kernel = np.ones((5,5),'int')
    maske = cv2.dilate(maske,kernel)
#cv2.inRange(hsv, altRenk, ustRenk) ile belirtilen renk aralığındaki pikselleri beyaz, diğerlerini siyah olarak içeren bir maske oluştururuz.
#np.ones((5, 5), 'int') ile 5x5 boyutunda, içi birlerle dolu bir numpy dizisi (kernel) oluştururuz.
#cv2.dilate(maske, kernel) ile maskeyi dilate ederiz, yani beyaz bölgedeki pikselleri genişletiriz.
    res = cv2.bitwise_and(kare,kare,mask=maske)
    konturlar = cv2.findContours(maske.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
#cv2.bitwise_and(kare, kare, mask=maske) ile orijinal kareyi maskeyle bitwise AND işlemi yaparak sadece maske alanını alırız.
#cv2.findContours(maske.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2] ile maske üzerindeki konturları buluruz.
    say = 0
#say değişkeni, belirli bir alan sınırlamasını geçen kontur sayısını temsil eder.
    for kontur in konturlar:
#konturlar listesindeki her kontur için döngüyü başlatır.
        alan = cv2.contourArea(kontur)
#cv2.contourArea(kontur) ile konturun alanını hesaplar.
        if alan > 600:
#Eğer konturun alanı 600'den büyükse:
            say+=1
#say değişkenini bir artırır.
            (x,y,w,h)=cv2.boundingRect(kontur)
            cv2.rectangle(kare, (x, y), (x + w, y + h), (0, 255, 0), 2)
#Konturun çevreleyen bir dikdörtgen oluşturarak çizim yapar.
            if cember:
                (x, y), ycap = cv2.minEnclosingCircle(kontur)
                merkez = (int(x), int(y))
                ycap = int(ycap)
                img = cv2.circle(kare, merkez, ycap, (255, 0, 0), 2)
#Eğer cember bayrağı True ise, konturun etrafında bir daire çizer.
    if say > 0:
        cv2.putText(kare, f'{say} {RENK} nesne bulundu', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, 1)
#Eğer say değişkeni sıfırdan büyükse, kare üzerine "say RENK nesne bulundu" yazısını yerleştirir.
    cv2.imshow('kare', kare)
    k = cv2.waitKey(4) & 0xFF
    if k == 27:
        break
#kare adlı pencerede kareyi görüntüler.
#Klavyeden bir tuşa basılıp basılmadığını kontrol eder. Eğer "ESC" tuşuna basıldıysa döngüyü sonlandırır.
if kamera.isOpened():
    kamera.release()
cv2.destroyAllWindows()
#Kamera yakalamayı durdurur ve pencereleri kapatır.

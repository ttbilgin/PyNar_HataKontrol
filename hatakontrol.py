#Import

import sqlite3
import subprocess
import sys
from pylint.lint import Run

#DEGISKENLER
VERITABANI_ISMI = "veri.db" #Sonunda .db olmali
TABLO_ISMI = "Hata_kodlari"
HATA_KODU_SUTUN = "Kod"
HATA_ACIKLAMA_SUTUN = "Aciklama"
CALISTIRMA_TEMEL_KOMUT = "pylint --msg-template='{msg_id}:{line}:{column}'"

class VTB:
	#VTB olustur
	def __init__(self):
		self.baglanti = sqlite3.connect(VERITABANI_ISMI)
		self.imlec = self.baglanti.cursor()
		tablo_baslat_komutu = "CREATE TABLE IF NOT EXISTS " + TABLO_ISMI + "(" + HATA_KODU_SUTUN + " TEXT PRIMARY KEY, " + HATA_ACIKLAMA_SUTUN + " TEXT)"
		self.imlec.execute(tablo_baslat_komutu)
		
	#Veritabaninda verilen hata kodlarini ara ve hata mesajlarini "returnle"
	def ara(self, liste):
		templist = []
		for i in liste:
			arama_kriteri = "SELECT " + HATA_ACIKLAMA_SUTUN + " FROM " + TABLO_ISMI + " WHERE " + HATA_KODU_SUTUN + "='" + i + "'"
			self.imlec.execute(arama_kriteri)
			temp = self.imlec.fetchone()
			if(temp):
				temp = temp[0]
			else:
				temp = "Hata veri tabaninda bulunamadi"
			templist.append(temp)
		return templist

def hata_al(dosya):
	islem = subprocess.run(CALISTIRMA_TEMEL_KOMUT + " " + dosya, capture_output = True)
	hata_listesi_bytes = islem.stdout
	hata_listesi = hata_listesi_bytes.decode().split("\r\n\r\n")[0]#Hata mesajinin son kismini cikar
	hata_listesi = hata_listesi.split("\r\n")[1:]#Elemenlara ayir
	hata_listesi = list(filter(None, hata_listesi))#Listeden bos elemenları cikar
	return hata_listesi

def hata_kodu_cikart(hata_kodu):
	liste = []
	for i in hata_kodu:
		kod = i.split(":")
		liste.append(kod[0])
	return liste

def hata_satirlari_cikart(hata_kodu):
	liste = []
	for i in hata_kodu:
		kod = i.split(":")
		liste.append(kod[1])
	return liste

if __name__ == "__main__":
	veri = VTB()
	for i in sys.argv[1:]:
		print(i + " dosyasi okunuyor")
		hatalar = hata_al(i)
		butun_hatalar = hata_kodu_cikart(hatalar)
		print(i + " Dosyasinda bu hatalar bulunmaktadir:")
		hata_raporu = veri.ara(butun_hatalar)
		hata_satirlari = hata_satirlari_cikart(hatalar)
		for k in range(len(hata_raporu)):
			print("Satir " + hata_satirlari[k] + ": " + hata_raporu[k])
		

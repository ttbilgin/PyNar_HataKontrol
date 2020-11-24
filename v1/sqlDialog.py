import datetime
import logging

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlRecord, QSqlTableModel

tablo_ismi = "Conversations"

def tablo_olustur():
    """if tablo_ismi in QSqlDatabase.database().tables():
        return""" 

    sorgu = QSqlQuery()
    if not sorgu.exec_(
        """
        CREATE TABLE IF NOT EXISTS 'Conversations' (
            'author' TEXT NOT NULL,
            'recipient' TEXT NOT NULL,
            'timestamp' TEXT NOT NULL,
            'message' TEXT NOT NULL,
        FOREIGN KEY('author') REFERENCES Contacts ( name ),
        FOREIGN KEY('recipient') REFERENCES Contacts ( name )
        )
        """
    ):
        logging.error("Veritabanı sorgulanamadı !")

    
    # Etkileşimli hale getirmek için geliştirme gereklidir.
    zaman_damgasi = datetime.datetime.now()
    sorgu.exec_(
        "INSERT INTO Conversations VALUES('machine', 'Me', '" + str(zaman_damgasi) +"', 'Nasıl Yardımcı olabilirim?')"
    )
    logging.info(sorgu)
    logging.debug('Ro-Bot: "{}"'.format("Nasıl Yardımcı olabilirim?"))


class SqlKonusmaModeli(QSqlTableModel):
    def __init__(self, parent=None):
        super(SqlKonusmaModeli, self).__init__(parent)

        tablo_olustur()
        self.setTable(tablo_ismi)
        self.setSort(2, Qt.DescendingOrder)
        self.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.recipient = ""

        self.select()
        logging.debug("Tablo başarı ile yüklendi.")
        
    
    def mesaj_ekle(self, mesaj, el_cevap):
        sorgu = QSqlQuery()
        zaman_damgasi = datetime.datetime.now()
        mesaj_ekle= "INSERT INTO Conversations (author,recipient,timestamp,message) VALUES ('machine', 'Me', '" + str(zaman_damgasi) +"', '" + str(mesaj) +"' )"
        cevap_ekle= "INSERT INTO Conversations (author,recipient,timestamp,message) VALUES ('machine', 'Me', '" + str(zaman_damgasi) +"', '" + str(el_cevap) +"' )"
        sorgu.exec_(mesaj_ekle)
        sorgu.exec_(cevap_ekle)
        logging.info(sorgu)
        logging.debug('Mesaj: "{}" mesajı Ro-Bot tarafindan alindi. '.format(mesaj))
        logging.debug('Mesaj: "{}" '.format(el_cevap))

    def setRecipient(self, recipient):
        if recipient == self.recipient:
            pass

        self.recipient = recipient

        filter_str = (
            "(recipient = '{}' AND author = 'Me') OR " "(recipient = 'Me' AND author='{}')"
        ).format(self.recipient)
        self.setFilter(filter_str)
        self.select()

    def data(self, index, rol):
        if rol < Qt.UserRole:
            return QSqlTableModel.data(self, index, rol)

        sql_kayit = QSqlRecord()
        sql_kayit = self.record(index.row())

        return sql_kayit.value(rol - Qt.UserRole)

    def roleNames(self):
        """dict degerini hash degerine  QSqlTableModel icin donusturur."""

        isimler = {}
        yazar = "author".encode()
        recipient = "recipient".encode()
        zaman_damgasi = "timestamp".encode()
        mesaj = "message".encode()

        isimler[hash(Qt.UserRole)] = yazar
        isimler[hash(Qt.UserRole + 1)] = recipient
        isimler[hash(Qt.UserRole + 2)] = zaman_damgasi
        isimler[hash(Qt.UserRole + 3)] = mesaj

        return isimler
		
    @Slot(str,str,str)
    def mesaj_yolla(self, recipient, mesaj, yazar):
        zaman_damgasi = datetime.datetime.now()
        yeni_kayit = self.record()
        yeni_kayit.setValue("author", yazar)
        yeni_kayit.setValue("recipient", recipient)
        yeni_kayit.setValue("timestamp", str(zaman_damgasi))
        yeni_kayit.setValue("message", mesaj)
        
        if not self.insertRecord(self.rowCount(), yeni_kayit):
            logging.error("Mesaj İletilemedi: {}".format(self.lastError().text()))
            return

        self.submitAll()
        self.select()

		

# -*- coding: utf-8 -*- 
import datetime
import logging
import re
import random

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlRecord, QSqlTableModel

pairs = [
    ['benim adım (.*)', ['merhaba %1']],
    ['(.*)adın (ne|nedir)?',['Ben ro-Bot. Sayın Prof. Dr. Turgay Tugay Bilgin in Tübitak projesi kapsamında geliştirilen bir chatbotum.']],
    [('merhaba|meraba|hey|hay'),['merhaba','heeey','naaber']],
    ['(.*) eğlenceli bir yer',['%1 gerçekten de çok eğlenceli bir yer']],
    ['(.*) (.*) oldukça (.*)',['%1 %2 gerçekten de çok %3']],
    ['(.*)nerede yaşıyorsun?',['Bursa\'da yaşıyorum.']],
    ['(.*)nerelisin?',['ben bir sohbet botuyum. doğum yerim yok.']],
    ['(.*)kaç yaşındasın ?',['2020 yılı itibari ile geliştirilmekteyim.']],
    ['(.*)hava nasıl ?',['her zamanki gibi. bir değişiklik yok!']],
    ['(.*)nasılsın ?',['ben çok iyiyim. sen nasılsın?']],
    ['(.*)yardım edermisin?',['elbette yardım ederim.']],
    ['boyun kaç?',['ben bir bot olduğum için boyum tanımsız.']],
    ['tamam',['görüşmek üzere']],
    ['(.*)',['Ne dediğinizi anlayamadım']],

]

reflections = {
    'nasılsın':'iyiyim',
    'ben':'sen',
    'benim':'senin',
    'benimki':'seninki'
}


class Chat(object):
    el_cevap =""
    def __init__(self, mesaj, pairs, reflections={}):

        """
        Chatbot'u başlatan fonksiyon. Pairs yanıtların ve cevapların listesidir.  Her kalıp, 
        kullanıcının ifadesi veya sorusuyla eşleşen normal bir ifadedir. Bu tür her model için olası yanıtların
        bir listesi verilir, örn. ['(.*)nasılsın ?', 'ben çok iyiyim. sen nasılsın?'].  Kalıpların parantezli bölümleri ile eşleşen ifadeler (örneğin: (.*))
        yanıtlardaki numaralandırılmış konumlara eşlenir, örnek olarak %1.

        :type pairs: Tuple listesi
        :param pairs: Kalıplar ve yanıtlar
        :type reflections: dict
        :param reflections: A mapping between first and second person expressions
        :rtype: None
        """
        
        self._pairs = [(re.compile(x, re.IGNORECASE), y) for (x, y) in pairs]
        self._reflections = reflections
        self._regex = self._compile_reflections()

    def _compile_reflections(self):
        sorted_refl = sorted(self._reflections, key=len, reverse=True)
        return re.compile(
            r"\b({0})\b".format("|".join(map(re.escape, sorted_refl))), re.IGNORECASE
        )

    def _substitute(self, str):
        """
        Reflections'ta belirtildiği gibi dizedeki kelimeleri değiştir.
        Örnnek olarak: "Ben" -> "Sen"

        :type str: str
        :param str: The string to be mapped
        :rtype: str
        """

        return self._regex.sub(
            lambda mo: self._reflections[mo.string[mo.start() : mo.end()]], str.lower()
        )

    def _wildcards(self, response, match):
        pos = response.find("%")
        while pos >= 0:
            num = int(response[pos + 1 : pos + 2])
            response = (
                response[:pos]
                + self._substitute(match.group(num))
                + response[pos + 2 :]
            )
            pos = response.find("%")
        return response

    def respond(self, str):
        """
        Kullanıcı girdisine bir yanıt oluştur.

        :type str: str
        :param str: The string to be mapped
        :rtype: str
        """

        # Her kalıbı kontrol et
        for (pattern, response) in self._pairs:
            match = pattern.match(str)

            # Eşleşen kalıp olduğunda
            if match:
                resp = random.choice(response)  # rastgele bir yanıt seç
                resp = self._wildcards(resp, match)

                # fix munged punctuation at the end
                if resp[-2:] == "?.":
                    resp = resp[:-2] + "."
                if resp[-2:] == "??":
                    resp = resp[:-2] + "?"
                return resp
                



    # Kullanıcı girişinin alındığı ve Chatbotun cevap verdiği sohbet fonksiyonu
    def converse(self, mesaj, quit="quit"):
        user_input = ""
        while user_input != quit:
            user_input = quit
            try:
                user_input = mesaj
            except EOFError:
                print("user_input")
            if user_input:
                while user_input[-1] in "!.":
                    user_input = user_input[:-1]
                self.el_cevap = self.respond(user_input)
                return self.el_cevap
                break
    
    def __repr__(self):
        return self.el_cevap

    


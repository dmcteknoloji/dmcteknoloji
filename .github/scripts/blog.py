"""README'deki blog listesini dmcteknoloji.com RSS akisindan tazeler.

Yalniz BLOG-BASLA / BLOG-BITIR isaretleri arasini degistirir. Akis
okunamazsa ya da bos donerse dosyaya dokunmaz (bos liste yayinlanmaz).
"""
import sys
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

AKIS = "https://www.dmcteknoloji.com/feed/"
DOSYA = "README.md"
ADET = 5
BAS, SON = "<!-- BLOG-BASLA -->", "<!-- BLOG-BITIR -->"

istek = urllib.request.Request(AKIS, headers={"User-Agent": "dmcteknoloji-profil"})
with urllib.request.urlopen(istek, timeout=30) as yanit:
    kok = ET.fromstring(yanit.read())

satirlar = []
for oge in kok.iter("item"):
    baslik = (oge.findtext("title") or "").strip()
    bag = (oge.findtext("link") or "").strip()
    tarih = oge.findtext("pubDate")
    if not baslik or not bag:
        continue
    gun = parsedate_to_datetime(tarih).strftime("%d.%m.%Y") if tarih else ""
    satirlar.append(f"- [{baslik}]({bag}) <sub>{gun}</sub>")
    if len(satirlar) == ADET:
        break

if not satirlar:
    sys.exit("akista yazi yok, README degistirilmedi")

metin = open(DOSYA, encoding="utf-8").read()
assert metin.count(BAS) == 1 and metin.count(SON) == 1, "isaretler eksik"
once, geri = metin.split(BAS)
_, sonra = geri.split(SON)
yeni = once + BAS + "\n" + "\n".join(satirlar) + "\n" + SON + sonra
if yeni != metin:
    open(DOSYA, "w", encoding="utf-8").write(yeni)
    print("guncellendi")
else:
    print("degisiklik yok")

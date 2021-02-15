"""
Miinaharava - lopputyö
Ohjelmoinnin alkeet, syksy 2019

Joona Meriläinen
"""

import random
import math
import sys
import datetime
import haravasto

HIIRENNAPIT = {
    haravasto.HIIRI_VASEN: "vasen",
    haravasto.HIIRI_OIKEA: "oikea"
}

asetukset = {
    "kenttaKokoX" : 0,
    "kenttaKokoY": 0,
    "miinaLkm": 0,
    "tulos": 0, #0 = kesken, 1 = voitto, 2 = häviö
    "tulosNimet": ["Kesken", "Voitto", "Häviö"],
    "lippuLkm": 0,
    "aloitusPaivaJaAika": "",
    "vuorot": 0
}

aika = {
    "sekunnit": 0,
    "minuutit": 0
}

kentta = {
    "alustaKentta": [],
    "peliKentta": []
}

def kasittele_hiiri(hiiriX, hiiriY, hiiriNappi, muokkaus):
    """
    Tätä funktiota kutsutaan kun käyttäjä klikkaa sovellusikkunaa hiirellä.
    """
    ruutuX = math.floor(hiiriX / 40)
    ruutuY = math.floor(hiiriY / 40)

    if asetukset["tulos"] == 0 and hiiriY < asetukset["kenttaKokoY"] * 40:
        if hiiriNappi == haravasto.HIIRI_VASEN:
            if kentta["peliKentta"][ruutuY][ruutuX] == " ":
                asetukset["vuorot"] += 1
                if kentta["alustaKentta"][ruutuY][ruutuX] == "x":
                    havio(ruutuX, ruutuY)
                elif isinstance(kentta["alustaKentta"][ruutuY][ruutuX], int):
                    kentta["peliKentta"][ruutuY][ruutuX] = kentta["alustaKentta"][ruutuY][ruutuX]
                elif kentta["alustaKentta"][ruutuY][ruutuX] == " ":
                    tulvataytto(ruutuX, ruutuY)
                    
        elif hiiriNappi == haravasto.HIIRI_OIKEA:
            if kentta["peliKentta"][ruutuY][ruutuX] == " ":
                kentta["peliKentta"][ruutuY][ruutuX] = "f"
                asetukset["lippuLkm"] += 1
            elif kentta["peliKentta"][ruutuY][ruutuX] == "f":
                kentta["peliKentta"][ruutuY][ruutuX] = " "
                asetukset["lippuLkm"] += 1
            
def tarkista_voitto():
    """
    Tarkistaa onko avaamattomia ruutuja yhtä paljon kuin miinoja
    """
    ruudut = asetukset["kenttaKokoX"] * asetukset["kenttaKokoY"]
    avatut = 0
    for y in range(len(kentta["peliKentta"])):
        for x in range(len(kentta["peliKentta"][y])):
            if kentta["peliKentta"][y][x] == "0" or isinstance(kentta["peliKentta"][y][x], int):
                avatut += 1
                
    if avatut == ruudut - asetukset["miinaLkm"] and asetukset["tulos"] == 0:
        voitto()
        
def toisto(kulunutAika):
    """
    Laskee peliajan
    """
    if asetukset["tulos"] == 0:
        aika["sekunnit"] += 1
        if aika["sekunnit"] == 60:
            aika["minuutit"] += 1
            aika["sekunnit"] = 0

def voitto():
    """
    Voitetun pelin jälkeen suoritettavat toiminnot
    """
    print("Voitit pelin!\n")
    asetukset["tulos"] = 1
    tallennaTilastot()

def havio(x, y):
    """
    Hävityn pelin jälkeen suoritettavat toiminnot
    """
    print("Hävisit pelin!\n")
    kentta["peliKentta"][y][x] = kentta["alustaKentta"][y][x]
    asetukset["tulos"] = 2
    tallennaTilastot()
    
def tallennaTilastot():
    """
    Tallentaa pelin tilastot tekstitiedostoon
    """
    with open("tilastot.txt", "a") as tilastot:
        tilastot.write("\n")
        tilastot.write("{} - {}\n".format(asetukset["aloitusPaivaJaAika"], asetukset["tulosNimet"][asetukset["tulos"]]))
        tilastot.write("Kenttä: {} x {}\n".format(asetukset["kenttaKokoX"], asetukset["kenttaKokoY"]))
        tilastot.write("Miinat: {} kpl\n".format(asetukset["miinaLkm"]))
        tilastot.write("Peliaika: {:02d}:{:02d}\n".format(aika["minuutit"], aika["sekunnit"]))
        tilastot.write("Käytetyt vuorot: {}\n".format(asetukset["vuorot"]))
        
def nayta_tilastot():
    """
    Tulostaa tilasto-tiedoston sisällön consoleen
    """
    sisalto = ""
    try:
        with open("tilastot.txt", "r") as sisalto:        
            print(sisalto.read())
    except FileNotFoundError:
        print("Tiedoston avaaminen epäonnistui")
    else:
        valikko(False)


def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()
    for yy in range(0, len(kentta["peliKentta"])):
        for xx in range(0, len(kentta["peliKentta"][yy])):
            haravasto.lisaa_piirrettava_ruutu(kentta["peliKentta"][yy][xx], xx * 40, yy * 40)
    haravasto.piirra_ruudut()
    
    tarkista_voitto()
    
    if asetukset["tulos"] == 0:
        if asetukset["kenttaKokoX"] > 2:
            haravasto.piirra_tekstia("{:02d}:{:02d}".format(aika["minuutit"], aika["sekunnit"]), 6, asetukset["kenttaKokoY"] * 40, (0, 0, 0, 255), "serif", 26)
        if asetukset["kenttaKokoX"] > 4:
            haravasto.piirra_tekstia("{:02d}".format(asetukset["miinaLkm"] - asetukset["lippuLkm"]), asetukset["kenttaKokoX"] * 40 - 43, asetukset["kenttaKokoY"] * 40, (0, 0, 0, 255), "serif", 26)
    else:
        if asetukset["kenttaKokoX"] > 3:
            if asetukset["tulos"] == 1:
                haravasto.piirra_tekstia("VOITIT", asetukset["kenttaKokoX"] * 40 / 2 - 60, asetukset["kenttaKokoY"] * 40, (50, 205, 50, 255), "serif", 26)
            elif asetukset["tulos"] == 2:
                haravasto.piirra_tekstia("HÄVISIT", asetukset["kenttaKokoX"] * 40 / 2 - 65, asetukset["kenttaKokoY"] * 40, (220, 20, 60, 255), "serif", 26)

def laske_miinat(x, y, kentta):
    """
    Laskee annetussa huoneessa yhden ruudun ympärillä olevat miinat ja palauttaa
    niiden lukumäärän.
    """
    miinat = 0
    for yy in range(y - 1, y + 2):
        for xx in range(x - 1, x + 2):
            if yy >= 0 and xx >= 0 and yy < len(kentta) and xx < len(kentta[y]) and kentta[yy][xx] == 'x':
                miinat += 1
    return miinat

def miinoita(vapaatRuudut, miinaLkm):
    """
    Asettaa kentällä miinaLkm kpl miinoja satunnaisiin ruutuihin.
    """
    for miinaNro in range(0, miinaLkm):
        valittu = vapaatRuudut[random.randrange(len(vapaatRuudut))]
        vapaatRuudut.remove(valittu)
        kentta["alustaKentta"][valittu[1]][valittu[0]] = "x"

def aseta_numerot():
    """
    Asettaa ruutua ympäröivien miinojen määrää ilmaisevan numeron kyseiselle ruudulle.
    """
    for y in range(0, len(kentta["alustaKentta"])):
        for x in range(0, len(kentta["alustaKentta"][y])):
            if not kentta["alustaKentta"][y][x] == "x" and not laske_miinat(x, y, kentta["alustaKentta"]) == 0:
                kentta["alustaKentta"][y][x] = laske_miinat(x, y, kentta["alustaKentta"])

def tulvataytto(xkoord, ykoord):
    """
    Merkitsee kentällä olevat tuntemattomat ruudut turvalliseksi siten, että
    täyttö aloitetaan annetusta x, y -pisteestä.
    """
    lista = []
    lista.append((xkoord, ykoord))
    
    while lista:
        kohta = lista.pop()
        
        if isinstance(kentta["alustaKentta"][kohta[1]][kohta[0]], int) and not kentta["peliKentta"][kohta[1]][kohta[0]] == "f":
            kentta["peliKentta"][kohta[1]][kohta[0]] = kentta["alustaKentta"][kohta[1]][kohta[0]]
        elif kentta["alustaKentta"][kohta[1]][kohta[0]] == " ":
            kentta["alustaKentta"][kohta[1]][kohta[0]] = "0"
            kentta["peliKentta"][kohta[1]][kohta[0]] = "0"
            for yy in range(kohta[1] - 1, kohta[1] + 2):
                for xx in range(kohta[0] - 1, kohta[0] + 2):
                    if yy >= 0 and xx >= 0 and yy < len(kentta["alustaKentta"]) and xx < len(kentta["alustaKentta"][kohta[1]]):
                        if not kentta["alustaKentta"][yy][xx] == "x" and not kentta["peliKentta"][yy][xx] == "f":
                            lista.append((xx, yy))

def luo_kentta(xKoko, yKoko, miinat):
    """
    Luo yKoko x xKoko kokoiset alusta- ja pelikentät
    """
    kentta["alustaKentta"] = []
    kentta["peliKentta"] = []
    for rivi in range(yKoko):
        kentta["alustaKentta"].append([])
        kentta["peliKentta"].append([])
        for sarake in range(xKoko):
            kentta["alustaKentta"][-1].append(" ")
            kentta["peliKentta"][-1].append(" ")

    jaljella = []
    for x in range(xKoko):
        for y in range(yKoko):
            jaljella.append((x, y))

    miinoita(jaljella, miinat)
    aseta_numerot()

def valikko(naytaVaihtoehdot):
    """
    Pelin päävalikko.
    """
    if naytaVaihtoehdot:
        print("\nMIINAHARAVA")
        
        print("1 - Uusi peli")
        print("2 - Tilastot")
        print("3 - Lopeta\n")
    
    while True:
        valinta = input("Valintasi: ")
        
        if valinta == "1":
            if not haravasto.grafiikka["ikkuna"] == None:
                haravasto.lopeta()
            uusi_peli()
        elif valinta == "2":
            nayta_tilastot()
        elif valinta == "3":
            sys.exit(0)
        else:
            print("Valintaa ei olemassa!") 

def uusi_peli():
    """
    Pyytää tarvittavat asetukset uuteen peliin ja kutsuu funktioita uuden pelin aloittamiseksi.
    """
    while True:
        try:
            asetukset["kenttaKokoX"] = int(input("Anna haluamasi kentän leveys ruutuina: "))
        except ValueError:
            print("Anna ruutujen määrä kokonaislukuna!")
        else:
            if(asetukset["kenttaKokoX"] > 2):
                break
            else:
                print("Liian pieni leveys!")
            
    while True:
        try:
            asetukset["kenttaKokoY"] = int(input("Anna haluamasi kentän korkeus ruutuina: "))
        except ValueError:
            print("Anna ruutujen määrä kokonaislukuna!")
        else:
            if(asetukset["kenttaKokoY"] > 2):
                break
            else:
                print("Liian pieni korkeus!")
            
    while True:
        try:
            asetukset["miinaLkm"] = int(input("Anna haluamasi miinojen määrä: "))
        except ValueError:
            print("Anna miinojen määrä kokonaislukuna!")
        else:
            if(asetukset["miinaLkm"] < asetukset["kenttaKokoX"] * asetukset["kenttaKokoY"]):
                break
            else:
                print("Liikaa miinoja!")
    
    reset()
    luo_kentta(asetukset["kenttaKokoX"], asetukset["kenttaKokoY"], asetukset["miinaLkm"])
    luo_ikkuna(kentta["peliKentta"])
    
def reset():
    """
    Resettaa muuttujat uutta peliä varten
    """
    asetukset["aloitusPaivaJaAika"] = ""
    asetukset["vuorot"] = 0
    aika["sekunnit"] = 0
    aika["minuutit"] = 0
    asetukset["tulos"] = 0
    asetukset["lippuLkm"] = 0

def luo_ikkuna(piirtoKentta):
    """
    Lataa pelin grafiikat, luo peli-ikkunan ja asettaa siihen piirtokäsittelijän.
    """
    haravasto.lataa_kuvat("./spritet/")
    haravasto.luo_ikkuna(len(piirtoKentta[0]) * 40, len(piirtoKentta) * 40 + 40)
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
    haravasto.aseta_toistuva_kasittelija(toisto, 1)
    asetukset["aloitusPaivaJaAika"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    haravasto.aloita()

if __name__ == "__main__":
    valikko(True)
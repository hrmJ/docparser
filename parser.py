from bs4 import BeautifulSoup 
from urllib.request import urlopen, Request
from parsepage import UbuntuHelpPage

class MultiLangDocu:
    """Koko dokumentaatio käyttäjän määrittelemistä aihepiireistä"""

    def __init__(self, langs):
        self.langs = langs
        self.clusters = list()
        self.data = dict()
        for lang in self.langs:
            self.data[lang] = list()

    def CreateClusters(themelist):
        """Luo teemoittaiset kokonaisuudet tallennettavaksi käännösmuisteiksi"""
        for theme in themelist:
            cl  = ThematicCluster(theme, self.langs)
            cl.GetPageList()
            cl.ParsePages()
            for lang in cl.langs:
                self.data.lang += cl.data[lang]


class ThematicCluster:
    """
    Kokonaisuus sivuista kaikilla halutuilla kielillä
    """

    def __init__(self, theme, langs):
        self.starturl = "https://help.ubuntu.com/lts/ubuntu-help/" + theme
        self.langs = langs
        self.data = dict()
        for lang in self.langs:
            self.data[lang] = list()
        self.pages = list()


    def GetPageList(self, start):
        """Hakee listan kaikista sivuista tässä kokonaisuudessa"""
        res = urlopen(start)
        soup = BeautifulSoup(res, 'lxml') 
        links=soup.findAll(["a"],{"class": "linkdiv"}) 
        for link in links: 
            self.pages.append("https://help.ubuntu.com/lts/ubuntu-help/" + link.get("href"))

    def ParsePages(self):
        """Jäsentää kunkin sivun ja kerää talteen teksti-informaation listamuodossa kappaleittain."""
        for page in self.pages:
            for lang in self.langs:
                q = Request(page)
                q.add_header("Accept-Language",lang)
                res=urlopen(q).read()
                parsed_page = UbuntuHelpPage(res)
                for p in parsed_page.paragraphs:
                    self.data[lang].append(p)



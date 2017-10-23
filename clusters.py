from bs4 import BeautifulSoup 
from urllib.request import urlopen, Request
from parsepage import UbuntuHelpPage, MsHelpPage
from tmx import Tmx
import pypandoc
from selenium import webdriver  
import time

class MultiLangDocu:
    """Koko dokumentaatio käyttäjän määrittelemistä aihepiireistä"""

    def __init__(self, langs):
        self.langs = langs
        self.clusters = list()
        self.data = dict()
        for lang in self.langs:
            self.data[lang] = list()

    def ParseCluster(self, theme):
        """Hae teemoittaiset kokonaisuudet tallennettavaksi käännösmuisteiksi"""
        cl  = ThematicCluster(theme, self.langs)
        cl.GetPageList()
        cl.ParsePages()
        sl="fi"
        for lang in cl.langs:
            if lang != sl:
                for tmxfile in cl.tmxdata[lang]:
                    with open("output/{}/{}_{}-{}.tmx".format(lang,tmxfile["name"],sl,lang),"w") as f:
                        f.write(tmxfile["content"])
                    print("Tallennettiin {}.tmx kielelle {}".format(tmxfile["name"],lang))

    def GetFilesFromCluster(self, theme):
        """Hae teemoittaiset kokonaisuudet tallennettavaksi tiedostoiksi"""
        cl  = ThematicCluster(theme, self.langs)
        cl.GetPageList()
        cl.GetPagesAsDocs()

class ThematicCluster:
    """
    Kokonaisuus sivuista kaikilla halutuilla kielillä
    """

    def __init__(self, theme, langs):
        self.starturl = "https://help.ubuntu.com/lts/ubuntu-help/" + theme
        self.langs = langs
        self.data = dict()
        self.datamodel = dict()
        self.tmxdata = dict()
        for lang in self.langs:
            self.datamodel[lang] = list()
            self.tmxdata[lang] = list()
        self.pages = list()
        self.pagenames = list()


    def GetPageList(self):
        """Hakee listan kaikista sivuista tässä kokonaisuudessa"""
        print("Fetching the pages in this thematic cluster.")
        res = urlopen(self.starturl)
        soup = BeautifulSoup(res, 'lxml') 
        links=soup.findAll(["a"],{"class": "linkdiv"}) 
        for link in links: 
            self.pages.append("https://help.ubuntu.com/lts/ubuntu-help/" + link.get("href"))
            self.pagenames.append(link.get("href").replace(".html",""))

    def GetPagesAsDocs(self):
        """Hakee kunkin sivun html:n ja konvertoi muihin tiedostomuotoihin"""
        sl = "fi"
        for idx, page in enumerate(self.pages):
            print("Parsing content in " + page)
            data=dict()
            for lang in self.langs:
                data[lang] = list()
                q = Request(page)
                q.add_header("Accept-Language",lang)
                res=urlopen(q).read()
                soup = BeautifulSoup(res, 'lxml') 
                content = soup.find("div",{"id":"content"})
                title = soup.find("span",{"class":"title"})
                fname = "output/documents/{}/{}_{}-{}.html".format(lang,self.pagenames[idx],sl,lang)
                with open(fname,"w") as f:
                    f.write("<h1>{}</h1>\n\n".format(title.text) + str(content))
                output = pypandoc.convert_file(fname, 'docx', outputfile=fname.replace(".html",".docx"))



    def ParsePages(self):
        """Jäsentää kunkin sivun ja kerää talteen teksti-informaation listamuodossa kappaleittain."""
        sl = "fi"
        for idx, page in enumerate(self.pages):
            print("Parsing content in " + page)
            data=dict()
            for lang in self.langs:
                data[lang] = list()
                q = Request(page)
                q.add_header("Accept-Language",lang)
                res=urlopen(q).read()
                parsed_page = UbuntuHelpPage(res)
                parsed_page.ParseContent()
                for p in parsed_page.segments:
                    data[lang].append(p)
            #Luodaan tmx-esitys sivusta
            this_tmx = Tmx(data[sl], sl)
            for tl in self.langs:
                if tl != sl:
                    self.tmxdata[tl].append({"name":self.pagenames[idx],"content":this_tmx.CreateSegments(data[tl],tl)})

def ParseMs(name, baseurl, langs):
    """
    Versio microsoftin help-sivuja varten

    baseurl: korvaa kieli merkkijonolla [@lang]
    """
    browser = webdriver.Chrome()  
    browser.implicitly_wait(3)
    pages = {}
    langcodes = {"en":"en-us","sv":"sv-se","fi":"fi-fi","fr":"fr-fr","de":"de-de","ru":"ru-ru"}
    data=dict()
    sl = "fi"
    for lang in langs:
        print(lang)
        data[lang]=list()
        browser.get(baseurl.replace("[@lang]",langcodes[lang]))
        time.sleep(1)  
        html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
        with open("/home/juho/Dropbox/pastebin/MS/{}_{}.html".format(name,lang),"w") as f:
            f.write(html)
        parsed_page = MsHelpPage(html)
        parsed_page.ParseContent()
        for p in parsed_page.segments:
            data[lang].append(p)
    this_tmx = Tmx(data[sl], sl)
    for tl in langs:
        if tl != sl:
            print("outputting " + tl)
            with open("output/MS/MICROSOFT_{}_{}-{}.tmx".format(name,sl,tl),"w") as f:
                f.write(this_tmx.CreateSegments(data[tl],tl))
    

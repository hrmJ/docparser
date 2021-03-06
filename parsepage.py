from bs4 import BeautifulSoup
import pypandoc

class UbuntuHelpPage:
    """Yksittäinen ubuntun helppisivu kielellä X"""

    def __init__(self, res):
        """Avaa sivu ja jäsennä bs:llä"""
        self.s = BeautifulSoup(res, 'lxml') 
        self.segments = list()

    def ParseContent(self):
        """Etsi kaikki varsinainen tekstisisältö"""
        paragraphs = self.s.findAll("p",{"class","p"})
        for p in paragraphs:
            self.segments.append(p.text)



class MsHelpPage(UbuntuHelpPage):
    """Yksittäinen windowsin helppisivu kielellä X"""

    def ParseContent(self):
        """Etsi kaikki varsinainen tekstisisältö"""
        paragraphs = self.s.findAll("p",{"class","ng-scope"})
        for p in paragraphs:
            self.segments.append(p.text)

    def ParseForOutput(self, lang, name):
        article = self.s.find("div",{"class":"content-article"})
        fname = "output/documents/MS/{}_{}.html".format(name,lang)
        with open(fname,"w") as f:
            f.write(str(article))
        output = pypandoc.convert_file(fname, 'docx', outputfile=fname.replace(".html",".docx"))




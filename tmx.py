from lxml import etree
import time


class Tmx():
    """Tmx-muotoinen esitys datasta"""

    def __init__(self, source_segments, source_lang):
        self.source_segments = source_segments
        self.sl = source_lang
        self.target_langs = dict()

    def CreateSegments(self, target_segments, lang):
        tmx = etree.Element("tmx")
        header = etree.SubElement(tmx,"header",{
                 "creationdate": time.strftime("%Y-%m-%d %H:%M"),
                 "srclang":"fi",
                 "adminlang":"fi",
                 "o-tmf":"unknown",
                 "segtype":"sentence",
                 "creationtool":"ByhrmJ",
                 "creationtoolversion":"unknown",
                 "datatype":"PlainText"})
        body = etree.SubElement(tmx, "body")
        for idx, segment in enumerate(target_segments):
            tu = etree.SubElement(body, "tu")
            sl = etree.SubElement(tu, "tuv", {"lang":self.sl})
            tl = etree.SubElement(tu, "tuv", {"lang":lang})
            slseg = etree.SubElement(sl, "seg")
            slseg.text = self.source_segments[idx]
            tlseg = etree.SubElement(tl, "seg")
            tlseg.text = segment.replace("\n","")
        return etree.tounicode(tmx, pretty_print=True)






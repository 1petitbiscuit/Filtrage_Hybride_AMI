import re
import dateparser

from .filtre_base import FiltreBase

class FiltreRegex(FiltreBase):

    def __init__(self, triggers, dossier_patterns):
        super().__init__()
        self.triggers = triggers
        self.dossier_patterns = dossier_patterns

    def filtre(self, text):
        texte_filtre  = text
        
        texte_filtre = re.sub(r"\b(?:\+1\s*)?(?:\(?\d{3}\)?[\s.-]*)\d{3}[\s.-]*\d{4}\b","[TÉLÉPHONE]",texte_filtre)
        texte_filtre = re.sub(r"\b\d{3}[- ]?\d{3}[- ]?\d{3}\b", "[NUMÉRO]", texte_filtre)
        texte_filtre = re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "[EMAIL]", texte_filtre)
        texte_filtre = re.sub(r"\b(?:\d{1,4}\s+)?(?:rue|avenue|av|boulevard|bd|chemin|ch|impasse|route|allée|place|quai)\s+[A-ZÉÈÊÂÀÙÎÔÇ][\w\s\'\-]*","[ADRESSE]",texte_filtre,flags=re.IGNORECASE)
        texte_filtre = re.sub(r"\d{3}.\d{3}.\d{2}.\d{2}", "[IP]", texte_filtre)
        texte_filtre = re.sub(r"\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b", "[MAC]", texte_filtre)
        texte_filtre = re.sub(r"\b(?:\d[ -]*?){13,16}\b", "[NUMÉRO]", texte_filtre)
        texte_filtre = re.sub(r"\b([A-Z]{3}[ -]?\d{3,4}|\d{3}[ -]?[A-Z]{3}|[A-Z]{1}\d{2}[ -]?[A-Z]{3}|[A-Z]{4}[ -]?\d{3})\b", "[NUMÉRO]", texte_filtre)
        texte_filtre = re.sub(r"\b[ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z][ -]?\d[ABCEGHJ-NPRSTV-Z]\d\b", "[NUMÉRO]", texte_filtre)
        texte_filtre = re.sub(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b", "[NUMÉRO]", texte_filtre)
        texte_filtre = re.sub(r"\b(?:"r"(?:\$|€|CAD|USD|dollars?|euros?|£|¥)\s?(?:\d{1,3}(?:[ .]\d{3})*|\d+)(?:[.,]\d{2})?"r"|"r"(?:\d{1,3}(?:[ .]\d{3})*|\d+)(?:[.,]\d{2})?\s?(?:\$|€|CAD|USD|dollars?|euros?|£|¥)"r")\b","[ARGENT]",texte_filtre)
        texte_filtre = re.sub(r"\b[A-Z]{2}\d{6,7}\b", "[NUMÉRO]", texte_filtre)
        texte_filtre = re.sub(r"\b[a-f0-9]{32,64}\b", "[NUMÉRO]", texte_filtre)
        

        self.regex_matched = False
        for mot in self.triggers:
            regex_mot = re.compile(rf"\b{mot}\b", re.IGNORECASE)
            if regex_mot.search(texte_filtre):
                self.regex_matched = True
                texte_filtre = regex_mot.sub("[INFOS_SENSIBLES]", texte_filtre)
        
            #check dossier/date
        for pattern in self.dossier_patterns:
            text = re.sub(pattern, "[NUMÉRO]", text, flags=re.IGNORECASE)
        
        
        for w in texte_filtre.split():
            if self.is_dossier(w):
                text = text.replace(w, "[NUMÉRO]")
            if self.is_date(w):
                text = text.replace(w, "[DATE]")
        
        self.set_content(texte_filtre)

    #~~ fonction ~~#
    @staticmethod
    def is_dossier(token):
        return (len(token) >= 5 and sum(c.isalpha() for c in token) and sum(c.isdigit() for c in token) and all(c.isalnum() or c in "-_#()[]" for c in token))

    @staticmethod
    def is_date(token):
        date = dateparser.parse(token, settings={"STRICT_PARSING": True}, languages=["fr"])
        return date is not None
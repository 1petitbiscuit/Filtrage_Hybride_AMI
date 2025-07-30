import spacy        #NLP; https://spacy.io/usage

from .filtre_base import FiltreBase

class FiltreNLP(FiltreBase):

    def __init__(self):
        super().__init__()
        self.nlp = spacy.load("fr_core_news_lg")     #sm = small, md = medium, lg = large
        
    
    def filtre(self, text):
        texte_filtre = text

        LABEL_MAPPING = {
        "PER": "PERSONNE",
        "ORG": "ORGANISATION",
        "DATE": "DATE",
        "TIME": "HEURE",
        "MONEY": "ARGENT"
        }
        
        doc = self.nlp(texte_filtre)
        for ent in doc.ents:
            if ent.label_ in LABEL_MAPPING:
                texte_filtre = texte_filtre.replace(ent.text, f"[{LABEL_MAPPING[ent.label_]}]")
        
        
        self.set_content(texte_filtre)
import spacy        #NLP; https://spacy.io/usage
import os

model_path = os.path.join( "NER", "model_output", "model-best")

from .filtre_base import FiltreBase

class FiltreNLP_Adresse(FiltreBase):

    def __init__(self):
        super().__init__()
        self.nlp_adresse = spacy.load(model_path)     #NLP entrainé pour reconnaitre les adresses
        
    
    def filtre(self, text):
        texte_filtre = text

        LABEL_MAPPING = {
        "PER": "PERSONNE",
        "ORG": "ORGANISATION",
        "DATE": "DATE",
        "TIME": "HEURE",
        "MONEY": "ARGENT"
        }
        
        doc = self.nlp_adresse(texte_filtre)
        for ent in doc.ents:
            if ent.label_  == "ADRESSE":
                texte_filtre = texte_filtre.replace(ent.text, "[ADRESSE]")
        
        if texte_filtre != text:
            self.sensibles_detectes.append("NLP_ADRESSE")
        
        self.set_content(texte_filtre)
from sentence_transformers import SentenceTransformer, util # type: ignore
from .filtre_base import FiltreBase

class FiltreSem(FiltreBase):

    def __init__(self, sementic_sensitive_phrases):
        super().__init__()
        self.sementic_sensitive_phrases = sementic_sensitive_phrases
        self.embed_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.sensitive_embeds = self.embed_model.encode(sementic_sensitive_phrases, convert_to_tensor=True)

        self.val_seuil_H = 0.7
        self.val_seuil_L = 0.65
        self.seuil_len_txt = 100

    def filtre(self, text):
        texte_filtre = text
        SEUIL_SIMILARITE = self.val_seuil_H if len(texte_filtre) < self.seuil_len_txt else self.val_seuil_L

        if not self.regex_matched:
            input_embed = self.embed_model.encode(texte_filtre, convert_to_tensor=True)
            cosine_scores = util.cos_sim(input_embed, self.sensitive_embeds)
            max_score = cosine_scores.max().item()

            if max_score >= SEUIL_SIMILARITE:
                texte_filtre += f"\n    [⚠️ ALERTE : contenu potentiellement sensible détecté par analyse sémantique]"
            
            texte_filtre += f"\n    [💡 Score de similarité sémantique détecté : {max_score:.2f}]"

            if texte_filtre != text:
                self.sensibles_detectes.append("Semantique")
            
            self.set_content(texte_filtre)
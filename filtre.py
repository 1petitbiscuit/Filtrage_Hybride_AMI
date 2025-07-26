import re           #regex
import spacy        #NLP; https://spacy.io/usage
import json
from sentence_transformers import SentenceTransformer, util # type: ignore
import tests_uni

#choix du modèle
nlp = spacy.load("fr_core_news_md")     #sm = small, md = medium, lg = large
embed_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

#gestion json
with open("JSON/triggers.json", "r", encoding="utf-8") as f:
    trigger_data = json.load(f)
with open("JSON/pat_dossier.json", "r", encoding="utf-8") as f:
    dossier_data = json.load(f)
with open("JSON/tests_unitaires.json", "r", encoding="utf-8") as f:
    tests_unitaires = json.load(f)

TRIGGERS = trigger_data["triggers"]
DOSSIER_PATTERNS = dossier_data["dossier_patern"]
SEMANTIC_SENSITIVE_PHRASES = trigger_data["sensitive_phrase"]
TESTS =  tests_unitaires["liste_test"]

SENSITIVE_EMBEDS = embed_model.encode(SEMANTIC_SENSITIVE_PHRASES, convert_to_tensor=True)

#seuil de déclenchement sémantique
SEUIL_SIMILARITE = 0.6


def filtre(text):
    original_text = text
    #~~~~ regex ~~~~
    text = re.sub(r"\d{3}-\d{3}-\d{4}", "[TÉLÉPHONE]", text)
    text = re.sub(r"\d{9}", "[NAS]", text)
    text = re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "[EMAIL]", text)
    text = re.sub(r"\d{1,4}\s+(rue|avenue|boulevard|chemin)\s+\w+", "[ADRESSE]", text, flags=re.IGNORECASE)

    for pattern in DOSSIER_PATTERNS:
        text = re.sub(pattern, "[NUMERO_DOSSIER]", text, flags=re.IGNORECASE)

    regex_matched = False
    for mot in TRIGGERS:
        regex_mot = re.compile(rf"\b{mot}\b", re.IGNORECASE)
        if regex_mot.search(text):
            regex_matched = True
            text = regex_mot.sub("[INFOS_SENSIBLES]", text)

    #~~~~ NLP ~~~~
    LABEL_MAPPING = {
    "PER": "PERSONNE",
    "LOC": "LIEU",
    "ORG": "ORGANISATION",
    "DATE": "DATE",
    "TIME": "HEURE",
    "MONEY": "ARGENT"
    }
    
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in LABEL_MAPPING:
            text = text.replace(ent.text, f"[{LABEL_MAPPING[ent.label_]}]")

    # ~~~~ Sémantique (embeddings)  ~~~~
    if not regex_matched:
        input_embed = embed_model.encode(original_text, convert_to_tensor=True)
        cosine_scores = util.cos_sim(input_embed, SENSITIVE_EMBEDS)
        max_score = cosine_scores.max().item()

        if max_score >= SEUIL_SIMILARITE:
            text += "\n[⚠️ ALERTE : contenu potentiellement sensible détecté par analyse sémantique]"
            print(f"💡 Score de similarité détecté : {max_score:.2f}")  #  optionnel

    
    return text


#~~~~~~~~~~~~#

def main():
    print("~~~~ Smulation entrée chatBot pour filtrage (NLP + regex) ~~~~")
    print("Taper (test) pour lancer ; Taper 'exit' pour quitter")

    while True:
        user_input = input(": ")
        if user_input.lower() in ["exit", "quit"]:
            print("Fin simulation")
            break
        if user_input.lower() in ["(test)", "(tests)"]:
            tests_uni.tester_filtre()

        output = filtre(user_input)
        print(f"Texte filtré : {output}\n")

if __name__ == "__main__":
    main()
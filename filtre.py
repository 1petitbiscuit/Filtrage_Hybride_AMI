import re           #regex
import spacy        #NLP; https://spacy.io/usage
from listes import Triggers, Patern_dossier

#choix du modèle
nlp = spacy.load("fr_core_news_md")     #sm = small, md = medium, lg = large


# Mots-clés sensibles


def filtre(text):
    #~~~~ regex ~~~~
    text = re.sub(r"\d{3}-\d{3}-\d{4}", "[TÉLÉPHONE]", text)
    text = re.sub(r"\d{9}", "[NAS]", text)
    text = re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "[EMAIL]", text)
    text = re.sub(r"\d{1,4}\s+(rue|avenue|boulevard|chemin)\s+\w+", "[ADRESSE]", text, flags=re.IGNORECASE)

    for pattern in Patern_dossier.DOSSIER_PATTERNS:
        text = re.sub(pattern, "[NUMERO_DOSSIER]", text, flags=re.IGNORECASE)

    for mot in Triggers.TRIGGERS:
        regex_mot = re.compile(rf"\b{mot}\b", re.IGNORECASE)
        text = regex_mot.sub("[INFOS_SENSIBLES]", text)

    #~~~~ NLP ~~~~
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ["PER", "LOC"]:
            text = text.replace(ent.text, f"[{ent.label_}]")
    
    return text


#~~~~~~~~~~~~#

def main():
    print("~~~~ Smulation entrée chatBot pour filtrage (NLP + regex) ~~~~")
    print("Taper 'exit pour quitter")

    while True:
        user_input = input(": ")
        if user_input.lower() in ["exit", "quit"]:
            print("Fin simulation")
            break
            
        output = filtre(user_input)
        print(f"Texte filtré : {output}\n")

if __name__ == "__main__":
    main()
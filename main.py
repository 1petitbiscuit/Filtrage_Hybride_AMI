import json

from py.filtre_regex import FiltreRegex
from py.filtre_nlp import FiltreNLP
from py.filtre_nlp_adresse import FiltreNLP_Adresse
from py.filtre_sem import FiltreSem
import py.tests_uni as test

#gestion json
with open("JSON/triggers.json", "r", encoding="utf-8") as f:
    trigger_data = json.load(f)
with open("JSON/tests_unitaires.json", "r", encoding="utf-8") as f:
    tests_unitaires = json.load(f)

TRIGGERS = trigger_data["triggers"]
DOSSIER_PATTERNS = trigger_data["dossier_patern"]
SEMANTIC_SENSITIVE_PHRASES = trigger_data["sensitive_phrase"]
TESTS =  tests_unitaires["liste_test"]

#~~~~#
regex_filtre = FiltreRegex(TRIGGERS, DOSSIER_PATTERNS)
sem_filtre = FiltreSem(SEMANTIC_SENSITIVE_PHRASES)
nlp_filtre = FiltreNLP()
#nlp_adresse_filtre = FiltreNLP_Adresse()

#~~ fonction ~~#
def filtre(text):
    temp_text = text
    #~~~~ regex ~~~~#
    regex_filtre.filtre(temp_text)
    temp_text = regex_filtre.get_result()

    #~~~~ NLP ~~~~#
    nlp_filtre.filtre(temp_text)
    temp_text = nlp_filtre.get_result()

    #~~~~ NLP adresse ~~~~#         non fonctionel
    #nlp_adresse_filtre.filtre(temp_text)
    #temp_text = nlp_adresse_filtre.get_result()


    # ~~~~ Sémantique (embeddings)  ~~~~#
    if len(text) > 20 :
        sem_filtre.filtre(temp_text)
        temp_text = sem_filtre.get_result()

    return temp_text

#~~~~~~~~~#

def main():
    print("~~~~ Smulation entrée chatBot pour filtrage (NLP + regex + sémantique) ~~~~")
    print("Taper (test) pour lancer ; Taper 'exit' pour quitter")

    while True:
        user_input = input(": ")
        if user_input.lower() in ["exit", "quit"]:
            print("Fin simulation")
            break
        if user_input.lower() in ["(test)", "(tests)"]:
            test.tester_filtre()
            continue

        output = filtre(user_input)
        print(f"Texte filtré : {output}\n")

if __name__ == "__main__":
    main()
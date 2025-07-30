import sys
sys.path.append("..")
from collections import Counter

import main

def tester_filtre():
    print("\n=== 📊 Lancement de la batterie de tests de filtrage ===\n")   
    tests = main.TESTS
    total = len(tests)
    correct = 0

    for i, test in enumerate(tests, 1):
        result = main.filtre(test["input"])
        expected_items = test["expected"]
        passed = True

        print(f"\n ---> Test {i} : {test['input']}")
        print(f"    🔍 Attendus : {expected_items}")
        print(f"    🧾 Résultat : {result}")

        if expected_items == []:        #check quand aucun filtrage attendu
            markers = [
                "[INFOS_SENSIBLES]", "[TÉLÉPHONE]", "[EMAIL]", "[NAS]", "[ADRESSE]",
                "[NUMERO_DOSSIER]", "[DATE]", "[HEURE]", "[ARGENT]", "[PERSONNE]",
                "ALERTE"
            ]
            for m in markers:
                if m in result:
                    passed = False
                    print(f"    ❌ Échec : présence inattendue de {m}")
                    break
        else:
            expected_counter = Counter(expected_items)
            result_counter = Counter()
            for item in expected_items:
                if item == "[INFOS_SENSIBLES_OR_ALERTE]":
                    if "[INFOS_SENSIBLES]" in result:
                        result_counter[item] = result.count("[INFOS_SENSIBLES]")
                    elif "ALERTE" in result:
                        result_counter[item] = 1
                    else:
                        result_counter[item] = 0
                elif item == "[ADRESSE_OR_ALERTE]":
                    if "[ADRESSE]" in result:
                        result_counter[item] = result.count("[ADRESSE]")
                    elif "[CODE_POSTAL]" in result:
                        result_counter[item] = result.count("[CODE_POSTAL]")
                    elif "ALERTE" in result:
                        result_counter[item] = 1
                    else:
                        result_counter[item] = 0
                elif item == "[NUMERO_DOSSIER_OR_ALERTE]":
                    if "[NUMERO_DOSSIER]" in result:
                        result_counter[item] = result.count("[NUMERO_DOSSIER]")
                    elif "[IP]" in result :
                        result_counter[item] = result.count("[IP]")
                    elif "[IMMATRICULATION]" in result :
                        result_counter[item] = result.count("[IMMATRICULATION]")
                    elif "[IBAN/SWIFT]" in result :
                        result_counter[item] = result.count("[IBAN/SWIFT]")
                    elif "[NUM_PASSEPORT]" in result :
                        result_counter[item] = result.count("[NUM_PASSEPORT]")
                    elif "[NUM_PERMIS_CONDUIRE]" in result :
                        result_counter[item] = result.count("[NUM_PERMIS_CONDUIRE]")
                    elif "[TOKEN]" in result :
                        result_counter[item] = result.count("[TOKEN]")
                    elif "ALERTE" in result:
                        result_counter[item] = 1
                    else:
                        result_counter[item] = 0
                else:
                    result_counter[item] = result.count(item)

                if result_counter[item] < expected_counter[item]:
                    passed = False
                    manquant = expected_counter[item] - result_counter[item]
                    print(f"    ❌ Échec : {item} attendu {expected_counter[item]} fois, trouvé {result_counter[item]} fois ({manquant} manquant)")
                    break

        if passed:
            correct += 1
            print("    ✅ Test réussi")
        else:
            print("    ❌ Test échoué")
        

    precision = (correct / total) * 100
    print("\n=== ✅ Résultats des tests ===")
    print(f"🎯 Précision : {precision:.2f}% ({correct}/{total} réussis)\n")


def count_occurrences(text, target):
    return text.count(target)
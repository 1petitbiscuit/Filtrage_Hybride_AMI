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
            alert_present = "ALERTE" in result

            for item in expected_items:
                found = result.count(item)
                if found >= expected_counter[item]:
                    result_counter[item] = found
                    continue
                elif alert_present:
                    print(f"    ⚠️ ALERTE présente — {item} manquant remplacé par ALERTE")
                    result_counter[item] = expected_counter[item]  # On le considère comme compensé
                    continue
                else:
                    passed = False
                    manquant = expected_counter[item] - found
                    print(f"    ❌ Échec : {item} attendu {expected_counter[item]} fois, trouvé {found} fois ({manquant} manquant)")
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
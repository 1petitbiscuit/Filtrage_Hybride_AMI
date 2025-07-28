import time
import filtre as fi


def tester_filtre():
    print("\n=== 📊 Lancement de la batterie de tests de filtrage ===\n")   
    tests = fi.TESTS
    total = len(tests)
    correct = 0

    for i, test in enumerate(tests, 1):
        result = fi.filtre(test["input"])
        expected_items = test["expected"]
        passed = True

        print(f"\n ---> Test {i} : {test['input']}")
        print(f"    🔍 Attendus : {expected_items}")
        print(f"    🧾 Résultat : {result}")

        if expected_items == []:
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
            for item in expected_items:
                if item == "[INFOS_SENSIBLES_OR_ALERTE]":
                    if "[INFOS_SENSIBLES]" not in result and "ALERTE" not in result:
                        passed = False
                        print("    ❌ Échec : ni [INFOS_SENSIBLES] ni ALERTE détecté")
                        break
                elif item == "[ADRESSE_OR_ALERTE]":
                    if "[ADRESSE]" not in result and "ALERTE" not in result:
                        passed = False
                        print("    ❌ Échec : ni [ADRESSE] ni ALERTE détecté")
                        break
                elif item == "[NUMERO_DOSSIER_OR_ALERTE]":
                    if "[NUMERO_DOSSIER]" not in result and "ALERTE" not in result:
                        passed = False
                        print("    ❌ Échec : ni [NUMERO_DOSSIER] ni ALERTE détecté")
                        break
                elif item not in result:
                    passed = False
                    print(f"    ❌ Échec : {item} non trouvé dans le résultat")
                    break

        if passed:
            correct += 1
            print("    ✅ Test réussi")
        else:
            print("    ❌ Test échoué")
        

    precision = (correct / total) * 100
    print("\n=== ✅ Résultats des tests ===")
    print(f"🎯 Précision : {precision:.2f}% ({correct}/{total} réussis)\n")

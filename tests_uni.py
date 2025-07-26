import time
import filtre as fi


def tester_filtre():
    print("\n=== 📊 Lancement de la batterie de tests de filtrage ===\n")   
    tests = fi.TESTS
    total = len(tests)
    correct = 0

    for i, test in enumerate(tests, 1):
        result = fi.filtre(test["input"])
        passed = False

        if test["expected"] in result:
            passed = True
        elif test["expected"] == "[INFOS_SENSIBLES_OR_ALERTE]":
            if "[INFOS_SENSIBLES]" in result or "ALERTE" in result:
                passed = True
        
        a = i/total*10
        b = a%1
        res = int(a-b)
        #affichage
        bar = "🟩" * res + "⬜" * (10 - res)
        status = "✅ SUCCÈS" if passed else "❌ ÉCHEC"
        print(f"[{bar}] ({i}/{total}) {status} : {test['input']} // ({test['difficulté']})")
        if not passed:
            print(f"    ↪ Résultat obtenu : {result}\n")
        if passed:
            correct += 1

        time.sleep(0.1)

    precision = (correct / total) * 100
    print("\n=== ✅ Tests terminés ===")
    print(f"🎯 Précision : {precision:.2f}% ({correct}/{total} réussis)\n")

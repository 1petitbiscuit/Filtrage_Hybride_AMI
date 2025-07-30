# FiltrageHybride\_NLP-regex

Prototype de filtrage pour l'outil AMI d'activis. Basé sur NLP et regex

PYTHON et JSON
Le fichier main.py exécute le programme. Le reste des fichiers python se trouve dans le répertoire "py".

"filtre_base.py" est une classe abstraite utilisé pour créer de nouveaux filtres.
"filtre_regex.py" contient le filtre regex.
"filtre_nlp.py" contient le filtre NLP.
"filtre_nlp_adresse.py" contient un filtre NLP entrainé (NER) utilisé pour découvrir des adresses dans les phrases. (Pas corretement fonctionnel)
"filtre_sem.py" contient le filtre sémantique.
Une liste des mots et phrases sensibles est stocké dans le répertoire "JSON" au nom de "triggers.json". Cette liste est utilisé pour énummérer tous les possibles déclancheurs d'alerte dans une requête AMI.

Les tests sont organisés dans le fichier "test_uni.py" et fait appel au fichier JSON "tests_unitaires.json", dans lequel se trouve la liste des tests.


REGEX
L'objectif de ce filtre est de capturé tout ce qui est formaté dans une requêtre.
Des rêgles peuvent être ajouté au filtre pour reconnaitre davantage de motifs pouvant être reconnu comme étant un renseignement personnel (ex: numéro de dossier, NAS, numéro de téléphone,...).

NLP
Au contraire, le NLP à pour but de filtrer en regardant le contexte. C'est à dire ce qui n'est pas formaté.
Une sélection de labels pouvant définir un renseignement personnel a été inqiqué comme "LABEL_MAPPING". Il est possible d'en rajouter d'autres dans la liste si jugé pertinent.
Le chargement du modèle se fait avec la ligne:
self.nlp = spacy.load("fr_core_news_md")
Medium est bon pour les prototypes. Mais dans l'idéal, il est recommandé d'utiliser un plus grand modèle pour plus de précision au prix de plus de temps de chargement. On a les terminaisons suivantes :
    - sm pour small
    - md pour medium
    - lg pour large

Sémantique
Un filtrage sémantique, plus basique que le NLP, a été ajouté en gage d'amélioration.
Plus il y a d'étapes de filtrages, plus on a de chances de capturer des renseignements personnels.

NER
Fichiers d'entrainements
Entrer dans train_data.jsonl les phrases à utiliser pour l'entrainement du modèle. Il est recommandé d'utiliser une bonne variété dans les exemples données. Plus il y a d'exemples, plus le modèle de language sera puissant.
Entrer dans dev_data.jsonl les phrases qui testeront le modèle pour juger de sa précision.
Un ratio 80% dans train_data et 20% dans dev_data est recommandé.
Convertir les données
SpaCy utilise des extensions .spacy pour lire ces fichiers d'entrainements. Il faut alors les convertir en exécutant le programme python convert_jsonl-spacy.py.
Le programme est prévu pour prendre des extensions .jsonl. Des fichiers .json classiques devront être convertit en premier lieu en .jsonl.
Fichier de configuration
Un fichier de configuration est déjà présent et peut être modifié si besoin. Nottament pour pointer vers d'autres fichiers d'entrainements en modifiant l'entrée [path] du fichier.
Un fichier de configuration peut être créé avec la commande :
python -m spacy init config config.cfg --lang fr --pipeline ner
Lancer l'entrainement
Pour lancer l'entrainement du modèle, on peut utiliser la commande suivante:
python -m spacy train config.cfg --output ./model_output --paths.train ./train_data.spacy --paths.dev ./dev_data.spacy
Les modèles entrainé sont alors déposé dans "NER/model_output/...".
Choix du modèle
Dans le code python, on charge alors le modèle NLP avec SpaCy. Le meilleur modèle entrainé sera stocké dans "model-best".



echo '```bash
# Lister les fichiers du répertoire courant
ls -la
```' >> README.md

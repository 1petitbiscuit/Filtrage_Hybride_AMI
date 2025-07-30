class FiltreBase:
    def __init__(self):
        self.texte_filtre = ""
        self.regex_matched = False
    
    def filtre(self, text):
        raise NotImplementedError("Chaque filtre enfant doit implémenter sa méthode filtrer")

    def set_content(self, text):
        self.texte_filtre = text

    def get_result(self):
        return self.texte_filtre

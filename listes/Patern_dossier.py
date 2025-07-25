DOSSIER_PATTERNS = [
    r"\b\d{6,10}\b",                                            # Numéro purement numérique (6 à 10 chiffres)
    r"\b[A-Z]{2,5}-?\d{4,10}\b",                                # Préfixe lettres (ex. FISC-123456, DOS123456)
    r"\b\d{4}[-/]\d{4,6}\b",                                    # Format année-numéro (ex. 2024-12345)
    r"\b(?:PLAINTES?|PL|AVIS|PERMIS|INT)[-\.]?\d{3,10}\b",      # Préfixe plainte ou permis
    r"\bID\d{5,10}\b",                                          # Identifiant générique type ID123456
    r"\bDOSS\d{4,10}\b",                                        # Format personnalisé "DOSS123456"
]
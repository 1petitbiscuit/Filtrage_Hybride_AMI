import spacy
from spacy.tokens import DocBin
import json

def convert_jsonl_to_spacy(jsonl_path, output_path, nlp):
    doc_bin = DocBin()
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            doc = nlp.make_doc(data['text'])
            ents = []
            for start, end, label in data['entities']:
                span = doc.char_span(start, end, label=label)
                if span is not None:
                    ents.append(span)
            doc.ents = ents
            doc_bin.add(doc)
    doc_bin.to_disk(output_path)

nlp = spacy.blank("fr")  # modèle vide pour structurer les données
convert_jsonl_to_spacy("train_data.jsonl", "train_data.spacy", nlp)
convert_jsonl_to_spacy("dev_data.jsonl", "dev_data.spacy", nlp)

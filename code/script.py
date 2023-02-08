import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import sys
import spacy_conll
import spacy_stanza
import torch
from transformers import AutoModel, AutoTokenizer
from function_definitions import txt_to_conll, get_contextual_embeddings
import json
dataset = sys.argv[1]  # the dataset which we will analyse



tokenizer = AutoTokenizer.from_pretrained("roberta-base")
model = AutoModel.from_pretrained("roberta-base")

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
model.to(device)

verb_embeddings = {}  # Dict[str, [List[torch.Tensor], List[torch.Tensor]]]

num_phrases, num_complex_phrases, num_negations, num_negations_in_dependent_clauses = 0, 0, 0, 0

for page in dataset:
    page_text = page['text']
    with open("current_page.conll", "w") as file:
        file.write(txt_to_conll(page_text, nlp))
    current_embeddings = get_contextual_embeddings("current_page.conll", tokenizer, model, device)

    # do any stats we need here

    for verb in current_embeddings:
        if verb not in verb_embeddings:
            verb_embeddings[verb] = current_embeddings[verb]
        else:
            verb_embeddings[verb] += current_embeddings[verb]

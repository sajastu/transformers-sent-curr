import glob
import json
import os
import re

from somajo import SoMaJo
import spacy

nlp = spacy.load("en_core_web_lg")
nlp.disable_pipe("parser")
nlp.enable_pipe("senter")
tokenizer = SoMaJo("en_PTB")


def sentencizer(text):
    sents = []
    doc = nlp(text)
    sent_lst = doc.sents
    for sent in sent_lst:
        sents.append(sent.text)
    return sents


cases = []

for f in glob.glob("blink/*.txt"):
    str = ''
    with open(f) as fR:
        for l in fR:
            str += l.strip().lower()
            str += ' '

    summary_sents = sentencizer(str)
    src_sentences_tkns = tokenizer.tokenize_text(summary_sents)


    iter = 0
    counter = 0
    src_tkns = []
    for j, sentence in enumerate(src_sentences_tkns):
        sent_tkns = []
        for token in sentence:
            sent_tkns.append(token.text)
        src_tkns.append(sent_tkns)
        counter += len(sent_tkns)

        if 900 < counter or j == len(src_sentences_tkns)-1:
            ent = {
                'id': f + f'-{iter}',
                'document': '</s><s> '.join([' '.join(s) for s in src_tkns]),
                'summary': 'This is the gold',
                'ext_labels': [0 for s in range(len(src_tkns))],
                'rg_labels': [0 for s in range(len(src_tkns))]
            }
            cases.append(ent)
            counter = 0
            iter +=1
            src_tkns = []

# os.makedirs('../blink_test_segmented/')
with open('../blink_test_segmented/test.json', mode='w') as fW:
    for e in cases:
        json.dump(e, fW)
        fW.write('\n')





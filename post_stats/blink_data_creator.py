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
src_tkns = []
iter = 0

for f in glob.glob("blink/*.txt"):
    str = ''
    token_counter = 0
    size = os.path.getsize(f)

    with open(f) as fR:

        for line_num, l in enumerate(fR):
            size -= len(l)
            if len(l.strip()) > 0 :
                str += l.strip()
                summary_sents = sentencizer(str)
                src_sentences_tkns = tokenizer.tokenize_text(summary_sents)
                token_count = sum(sum(1 for t in s) for s in src_sentences_tkns)

                # if token_count > 350 or l.strip() == fR.readlines()[-1].strip():
                if not size:
                    print('yohoo last line')
                if token_count > 200 or not size:
                    src_sentences_tkns = tokenizer.tokenize_text(summary_sents)

                    # should store
                    for j, sentence in enumerate(src_sentences_tkns):
                        sent_tkns = []
                        for token in sentence:
                            sent_tkns.append(token.text.lower())
                        src_tkns.append(sent_tkns)

                    ent = {
                        'id': f + f'-{iter}',
                        'document': '</s><s> '.join([' '.join(s) for s in src_tkns]),
                        'summary': 'This is the gold',
                        'ext_labels': [0 for s in range(len(src_tkns))],
                        'rg_labels': [0 for s in range(len(src_tkns))]
                    }
                    cases.append(ent)
                    counter = 0
                    iter += 1
                    src_tkns = []
                    str = ''

                else:
                    str += ' '
                    src_tkns = []

                    continue


    # summary_sents = sentencizer(str)
    # src_sentences_tkns = tokenizer.tokenize_text(summary_sents)
    # sent_num = sum(1 for _ in src_sentences_tkns)
    # src_sentences_tkns = tokenizer.tokenize_text(summary_sents)


# os.makedirs('../blink_test_segmented/')
with open('../blink_test_segmented/test.json', mode='w') as fW:
    for e in cases:
        json.dump(e, fW)
        fW.write('\n')





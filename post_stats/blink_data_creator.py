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

def _get_ngrams(n, text):
    """Calcualtes n-grams.
    Args:
      n: which n-grams to calculate
      text: An array of tokens
    Returns:
      A set of n-grams
    """
    ngram_set = set()
    text_length = len(text)
    max_index_ngram_start = text_length - n
    for i in range(max_index_ngram_start + 1):
        ngram_set.add(tuple(text[i:i + n]))
    return ngram_set


def _get_word_ngrams(n, sentences):
    """Calculates word n-grams for multiple sentences.
    """
    assert len(sentences) > 0
    assert n > 0

    # words = _split_into_words(sentences)

    words = sum(sentences, [])
    # words = [w for w in words if w not in stopwords]
    return _get_ngrams(n, words)


def cal_rouge(evaluated_ngrams, reference_ngrams):
    reference_count = len(reference_ngrams)
    evaluated_count = len(evaluated_ngrams)

    overlapping_ngrams = evaluated_ngrams.intersection(reference_ngrams)
    overlapping_count = len(overlapping_ngrams)

    if evaluated_count == 0:
        precision = 0.0
    else:
        precision = overlapping_count / evaluated_count

    if reference_count == 0:
        recall = 0.0
    else:
        recall = overlapping_count / reference_count

    f1_score = 2.0 * ((precision * recall) / (precision + recall + 1e-8))
    return {"f": f1_score, "p": precision, "r": recall}


def greedy_selection(doc_sent_list, abstract_sent_list, summary_size):
    def _rouge_clean(s):
        return re.sub(r'[^a-zA-Z0-9 ]', '', s)

    max_rouge = 0.0
    abstract = sum(abstract_sent_list, [])
    abstract = _rouge_clean(' '.join(abstract)).split()
    sents = [_rouge_clean(' '.join(s)).split() for s in doc_sent_list]
    evaluated_1grams = [_get_word_ngrams(1, [sent]) for sent in sents]
    reference_1grams = _get_word_ngrams(1, [abstract])
    evaluated_2grams = [_get_word_ngrams(2, [sent]) for sent in sents]
    reference_2grams = _get_word_ngrams(2, [abstract])

    selected = []
    for s in range(summary_size):
        cur_max_rouge = max_rouge
        cur_id = -1
        for i in range(len(sents)):
            if (i in selected):
                continue
            c = selected + [i]
            candidates_1 = [evaluated_1grams[idx] for idx in c]
            candidates_1 = set.union(*map(set, candidates_1))
            candidates_2 = [evaluated_2grams[idx] for idx in c]
            candidates_2 = set.union(*map(set, candidates_2))
            rouge_1 = cal_rouge(candidates_1, reference_1grams)['f']
            rouge_2 = cal_rouge(candidates_2, reference_2grams)['f']
            rouge_score = rouge_1 + rouge_2
            if rouge_score > cur_max_rouge:
                cur_max_rouge = rouge_score
                cur_id = i
        if (cur_id == -1):
            # return selected
            break
        selected.append(cur_id)
        max_rouge = cur_max_rouge

    retrun_bin_labels = []
    for i, s in enumerate(doc_sent_list):
        if i in selected:
            retrun_bin_labels.append(1)
        else:
            retrun_bin_labels.append(0)

    # return sorted(selected)
    return retrun_bin_labels, sorted(selected)


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
    with open(f):
        for l in f:
            str += l.strip().lower()
            str += ' '

    summary_sents = sentencizer(str)
    src_sentences_tkns = tokenizer.tokenize_text(summary_sents)

    src_tkns = []
    for sentence in src_sentences_tkns:
        sent_tkns = []
        for token in sentence:
            sent_tkns.append(token.text)
        src_tkns.append(sent_tkns)

    # ext_labels, selected_sent_ids = greedy_selection(src_tkns, ['this', 'is', 'the', 'target'], 1)
    ent = {
        'document': '</s><s> '.join(src_tkns),
        'summary': 'This is the gold',
        'ext_labels': [0 for s in range(len(src_tkns))],
        'rg_labels': [0 for s in range(len(src_tkns))]
    }
    cases.append(ent)


os.makedirs('../blink_test/')
with open('../blink_test/test.json', mode='w') as fW:
    for e in cases:
        json.dump(e, fW)
        fW.write('\n')





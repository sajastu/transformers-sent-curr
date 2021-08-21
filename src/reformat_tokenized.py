import glob
import json
import os
import random
import re
from multiprocessing import Pool

from tqdm import tqdm

from somajo import SoMaJo

from multiSumm.oracle_rouge import _get_word_ngrams, cal_rouge, greedy_selection
from others.utils import clean

tokenizer = SoMaJo("en_PTB")

TOKENIZED_DIR = '/home/code-base/lrg_split_machines/tokenized-m0/'


def _mp_m_process(param):
    ent = param
    src_sents = ent['document']
    src_tkns = []
    for sent in src_sents:
        src_sentences_tkns = tokenizer.tokenize_text([sent])
        ctr = 0
        for _ in src_sentences_tkns: ctr += 1
        src_sentences_tkns_tmp = []
        if ctr > 1:
            src_sentences_tkns = tokenizer.tokenize_text([sent])
            for sT in src_sentences_tkns:
                for tkn in sT:
                    src_sentences_tkns_tmp.append(tkn.text)
            src_sentences_tkns = src_sentences_tkns_tmp
        else:
            src_sentences_tkns = tokenizer.tokenize_text([sent])
            for sT in src_sentences_tkns:
                for tkn in sT:
                    src_sentences_tkns_tmp.append(tkn.text)
            src_sentences_tkns = src_sentences_tkns_tmp

        sent_tkns = []
        for token in src_sentences_tkns:
            sent_tkns.append(token)
        src_tkns.append(sent_tkns)

    summary_sents = ent['summary']
    tgt_sentences_tkns = tokenizer.tokenize_text(summary_sents)

    tgt_tkns = []
    for sentence in tgt_sentences_tkns:
        sent_tkns = []
        for token in sentence:
            sent_tkns.append(token.text)
        tgt_tkns.append(sent_tkns)

    ext_labels, selected_sent_ids = greedy_selection(src_tkns, tgt_tkns, 3)
    assert len(ext_labels) == len(src_sents), '`ext_labels` and `src_sents` should have same size'
    assert ext_labels is not None, '`ext_labels` should not be uninitialized'
    ent['ext_labels'] = ext_labels

    # ext_summary = ' '.join([s for j, s in enumerate(src_sents) if j in selected_sent_ids])

    return ent


def load_json(p, lower):
    source = []
    tgt = []
    flag = False
    for sent in json.load(open(p))['sentences']:
        tokens = [t['word'] for t in sent['tokens']]
        if (lower):
            tokens = [t.lower() for t in tokens]
        if (tokens[0] == '@highlights'):
            flag = True
            tgt.append([])
            continue
        if (flag):
            tgt[-1].extend(tokens)
        else:
            source.append(tokens)

    source = [clean(' '.join(sent)).split() for sent in source]
    tgt = [clean(' '.join(sent)).split() for sent in tgt]
    return source, tgt, p.split('/')[-1]


def _format_to_lines(params):
    f = params
    try:
        source, tgt, id = load_json(f, True)
        ent = {
            'id': id,
            'document': [' '.join(s) for s in source if len(s) > 4],
            'summary': [' '.join(t) for t in tgt]
        }

        new_ent = _mp_m_process(ent)

        # if len(new_ent['ext_labels']) > 2: #only retain those who have more than 3 src sents
        new_ent['document'] = '</s><s> '.join([' '.join(s).encode("ascii", "ignore").decode() for s in source if len(s) > 4])
        new_ent['summary'] = ' '.join([' '.join(t).encode("ascii", "ignore").decode() for t in tgt])


        return new_ent
    except:
        return None
    # else:
    #     return None

def format_to_lines(args):

    # check if save_path exists
    if not os.path.exists(args['save_path']):
        os.makedirs(args['save_path'])

    a_lst = []
    # split 95-5

    for inp in args['input_file_dir']:
        for f in glob.glob(inp + '/*'):
            a_lst.append(f)
        # ent = _format_to_lines(a_lst[-1])
    set_count_mapping = {
        'train': int(.95 * len(a_lst)),
        'valid': int(.025 * len(a_lst)),
        'test': int(.025 * len(a_lst)),
        # 'valid': int(.05 * len(os.listdir(args['input_file_dir'])))
    }
    pool = Pool(70)
    dataset = []
    p_ct = 0
    random.seed(8080)
    random.shuffle(a_lst)
    current_set = 'train'
    gathered = {
        'train': 0,
        'valid': 0,
        'test':0
    }
    # a_lst = a_lst[1550062:]
    for d in tqdm(pool.imap_unordered(_format_to_lines, a_lst), total=len(a_lst)):
        if d is not None:
            dataset.append(d)
            set_count_mapping[current_set] -= 1
            if (len(dataset) > args['shard_size']):
                pt_file = "{:s}{:s}.{:d}.json".format(args['save_path'], current_set, p_ct)
                gathered[current_set] += len(dataset)
                with open(pt_file, 'w') as save:
                    for d in dataset:
                        json.dump(d, save)
                        save.write('\n')
                    p_ct += 1
                    dataset = []
            # if set_count_mapping[current_set] == 0:
            #     break

            if set_count_mapping[current_set] == 0 and current_set == 'test':
                break

            if set_count_mapping[current_set] == 0 and current_set == 'train':
                if (len(dataset) > 0):
                    pt_file = "{:s}{:s}.{:d}.json".format(args['save_path'], current_set, p_ct)
                    gathered[current_set] += len(dataset)
                    with open(pt_file, 'w') as save:
                        for d in dataset:
                            json.dump(d, save)
                            save.write('\n')
                        p_ct += 1
                        dataset = []
                current_set = 'valid'

            if set_count_mapping[current_set] == 0 and current_set == 'valid':
                if (len(dataset) > 0):
                    pt_file = "{:s}{:s}.{:d}.json".format(args['save_path'], current_set, p_ct)
                    gathered[current_set] += len(dataset)
                    with open(pt_file, 'w') as save:
                        for d in dataset:
                            json.dump(d, save)
                            save.write('\n')
                        p_ct += 1
                        dataset = []
                current_set = 'test'

    pool.close()
    pool.join()

            # if set_count_mapping[current_set] == 0 and current_set != 'valid':
            #     current_set = 'valid'
            #
            # if set_count_mapping[current_set] == 0 and current_set == 'valid':
            #     break

    pool.close()
    pool.join()

    if (len(dataset) > 0):
        pt_file = "{:s}{:s}.{:d}.json".format(args['save_path'], current_set, p_ct)
        gathered[current_set] += len(dataset)
        with open(pt_file, 'w') as save:
            for d in dataset:
                json.dump(d, save)
                save.write('\n')
            p_ct += 1
            dataset = []

    print(f'Gathered: Train {gathered["train"]} -- Validation {gathered["valid"]}')

if __name__ == '__main__':
    format_to_lines(
        {
            'input_file_dir': ['/home/code-base/lrg_split_machines/tokenized_m-2021/'],
            'save_path': '/home/code-base/lrg_split_machines/dataset-m2021/',
            'shard_size': 25000
        }
    )

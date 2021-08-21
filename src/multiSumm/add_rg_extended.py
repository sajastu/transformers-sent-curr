import json
import os
from multiprocessing import Pool
from os.path import join as pjoin

from datasets import load_metric
from tqdm import tqdm

BASE_DIR_OLD = '/home/code-base/user_space/packages/datasets/reddit_tifu_segmented-ext-wRg'
BASE_DIR = '/home/code-base/user_space/packages/datasets/reddit_tifu_enhanced-ext'
WRITE_DIR = BASE_DIR + '-wRg'

if not os.path.exists(WRITE_DIR):
    os.makedirs(WRITE_DIR)

metric = load_metric("rouge")


def _mp_labelling(params):
    ent, rg_labels = params

    # if rg_labels != 'none' and len(rg_labels) == len(ent['ext_labels']):
    #     ent['rg_labels'] = rg_labels
    #     return ent
    # else:
    src_sents = [s.strip() for s in ent['document'].split('</s><s> ')]
    rg_labels = []
    rg1_labels = []
    for sent in src_sents:
        result = metric.compute(predictions=[sent], references=[ent['summary']], use_stemmer=True)
        # Extract a few results from ROUGE
        result = {key: value.mid.fmeasure for key, value in result.items()}
        rg_labels.append((result['rouge2'] + result['rougeL']) / 2)
        rg1_labels.append(result['rouge1'])

    if sum(rg_labels) > 0:
        rg_labels = [r / sum(rg_labels) for r in rg_labels]
    else:
        print(str(rg_labels) + ' ' + 'rg1 starts...')
        rg_labels = rg1_labels
        if sum(rg_labels) > 0:
            rg_labels = [r / sum(rg_labels) for r in rg_labels]
        else:
            print(str(rg_labels) + ' ' + 'rg1 not submitted...')
            rg_labels = [0 for r in rg_labels]

        ent['rg_labels'] = rg_labels
        return ent


for set in ['train']:
    old_instances = []
    old_ids = []
    new_ids = []
    new_instances = []
    i = 0

    exisiting_instances = []
    exisiting_ids = []
    with open(pjoin(BASE_DIR_OLD, set+ '.json')) as fRR:
        for li in fRR:
            exisiting_instances.append(json.loads(li)['rg_labels'])
            exisiting_ids.append(json.loads(li)['id'].replace('train-i', 'train-'))

    with open(pjoin(BASE_DIR, set + '.json')) as fR:
        n_lines = sum([1 for _ in open(pjoin(BASE_DIR, set + '.json'))])
        for li in tqdm(fR, total=n_lines):
            ent = json.loads(li)
            # if 'id' not in ent.keys():
            #     ent['id'] = f'{set}-i{i}'
            #     i += 1
            if ent['id'] in exisiting_ids:
                old_instances.append((ent, exisiting_instances[exisiting_ids.index(ent['id'])]))
            else:
                old_instances.append((ent, 'none'))

            old_ids.append(ent['id'])

        pool = Pool(90)

        for ent in tqdm(pool.imap_unordered(_mp_labelling, old_instances), total=len(old_instances)):
            new_instances.append(ent)
            new_ids.append(ent['id'])

        n_new_instances = []

        for oId in old_ids:
            new_index = new_ids.index(oId)
            n_new_instances.append(new_instances[new_index])

    with open(pjoin(WRITE_DIR, set + '.json'), mode='w') as fW:
        for n in n_new_instances:
            json.dump(n, fW)
            fW.write('\n')

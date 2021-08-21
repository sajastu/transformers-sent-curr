import glob

# all_ids = []
# for f in glob.glob('//home/code-base/mashine_split_lrg_reddit/m_1/*'):
#     all_ids.append(f.split('/')[-1].replace('.json', ''))
#
# with open('m1_ids.txt', mode='w') as fW:
#     for a in all_ids:
#         fW.write(a)
#         fW.write('\n')
#
import json
from bisect import bisect_left
from multiprocessing import Pool, cpu_count

from tqdm import tqdm


def bi_contains(lst, item):
    """ efficient `item in lst` for sorted lists """
    # if item is larger than the last its not in the list, but the bisect would
    # find `len(lst)` as the index to insert, so check that first. Else, if the
    # item is in the list then it has to be at index bisect_left(lst, item)
    return (item <= lst[-1]) and (lst[bisect_left(lst, item)] == item)

def _mp_write(params):
    fname, text = params

    with open(f'/home/code-base/m3/{fname}', mode='w') as fW:
        fW.write(text)

retrieved_ids = []
for split in ['m0', 'm1', "m2", "m4"]:
    with open(f'{split}_ids.txt') as fR:
        for l in fR:
            retrieved_ids.append(l.strip())

retrieved_ids = sorted(retrieved_ids)

all_ids = []

allc=0
alls=0
for set in ["test", "validation", "train"]:
    with open(f'/home/code-base/tldr_dataset/{set}.json') as fR:
        for l in tqdm(fR):
            ent = json.loads(l.strip())
            id = ent['id']
            if not bi_contains(retrieved_ids, f'{set}-' + id):
                src = ent['src'].replace('\n',' ')
                tgt = ent['tldr'].replace('\n',' ')
                all_ids.append((f'{set}-' + id, src + '\n' + '@highlights' + '\n' + tgt))
                alls+=1
            allc+=1

        print(f'{split} --- {alls/allc}')
        alls=0
        allc=0
            # all_ids.append(id)

pool = Pool(cpu_count())
for _ in tqdm(pool.imap_unordered(_mp_write, all_ids), total=len(all_ids)):
    pass

import glob
import json
import pickle
from multiprocessing import Pool, cpu_count

from tqdm import tqdm

from utils.rouge_score import evaluate_rouge


def _mp_rg(input_file):
    return_rgs = {}
    with open(input_file) as fR:
        for l in tqdm(fR):
            ent = json.loads(l.strip())
            src, tgt = ent['document'], ent['summary']

            src_sents = src.split('</s><s> ')
            rouge_scores = []
            for sent in src_sents:
                rgs = evaluate_rouge([sent], [tgt])
                rouge_scores.append((rgs[1] + rgs[2])/2)
            return_rgs[ent['id']] = rouge_scores
    return return_rgs


def select_highQ(params):
    input_dir, out_pkl = params['input_file_dir'], params['save_path']

    input_files = []
    for f in glob.glob(input_dir + '/*.json'):
        input_files.append(f)
        # _mp_rg(f)

    rg_labels = {}

    pool = Pool(cpu_count())
    for rg_label in tqdm(pool.imap_unordered(_mp_rg, input_files), total=len(input_files)):
        for key, val in rg_label.items():
            rg_labels[key] = val

    with open(out_pkl, 'wb') as handle:
        pickle.dump(rg_labels, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    select_highQ(
        {
            'input_file_dir': '/home/code-base/lrg_split_machines/dataset-m1/',
            'save_path': '/home/code-base/lrg_split_machines/dataset-m1/rg_score_m1.pkl',
        }
    )

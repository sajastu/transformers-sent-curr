import glob
import json
import os
import shutil

from tqdm import tqdm
DS_DIR="/home/code-base/tldr_dataset/"

# for set in ["test", "validation", "train"]:
#     os.makedirs(DS_DIR + 'splits/' + set)
#     single_files_dir = DS_DIR + 'splits/' + set
#     num_lines = sum([1 for l in open(DS_DIR + set + '.json')])
#     with open(DS_DIR + set + '.json') as fR:
#         for l in tqdm(fR, total=num_lines, desc=set):
#             ent = json.loads(l.strip())
#             with open(single_files_dir + '/' + f'{set}-ent["id"]', mode='w') as fW:
#                 fW.write(ent['src'] + '\n')
#                 fW.write('@highlights\n')
#                 fW.write(ent['tldr'])


for set in ["test", "validation", "train"]:
    single_files_dir = DS_DIR + 'splits/' + set
    for f in tqdm(glob.glob(DS_DIR + f'/splits/{set}/*.json'), total=len(glob.glob(DS_DIR + f'/splits/{set}/*.json'))):
        with open(f) as fR:
            for l in fR:
                ent = json.loads(l.strip())
                with open(single_files_dir + '/' + f'{set}-ent["id"]', mode='w') as fW:
                    fW.write(ent['src'] + '\n')
                    fW.write('@highlights\n')
                    fW.write(ent['tldr'])
        os.remove(f)

# for set in ["test", "validation", "train"]:
# for set in ["train"]:
#     for f in tqdm(glob.glob(DS_DIR + f'/splits/{set}/*.json'), total=len(glob.glob(DS_DIR + f'/splits/{set}/*.json'))):
#         # shutil.move(f, '/home/code-base/tldr_dataset/20-21-tldrs/tldr_data_p2/')
#         os.remove(f)
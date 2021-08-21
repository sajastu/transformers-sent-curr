import json

BASE_DIR = "/home/code-base/user_space/packages/datasets/reddit_tifu_segmented-ext/"

for set in ["train", "validation", "test"]:

    with open(BASE_DIR + set + '.json') as fR:
        for l in fR:
            ent = json.loads(l.strip())

            src_sents_len = len(ent['document'].split('</s><s>'))
            ext_labels_len = len(ent['ext_labels'])


            if src_sents_len != ext_labels_len:
                print(ent['id'])

import json
import os
import re
from multiprocessing import Pool

from somajo import SoMaJo
import spacy
from spacy.language import Language
from tqdm import tqdm

from transformers import AutoTokenizer

nlp = spacy.load("en_core_web_lg")
# nlp.disable_pipe("parser")
# nlp.enable_pipe("senter")

boundary = re.compile('^[0-9]$')

tokenizer = AutoTokenizer.from_pretrained(
    'facebook/bart-large',
    cache_dir=None,
    use_fast=False,
    revision='main',
    use_auth_token=None,
)


@Language.component("my_component")
def my_component(doc):
    prev = doc[0].text
    length = len(doc)
    for index, token in enumerate(doc):
        if (token.text == '.' and boundary.match(prev) and index != (length - 1)):
            doc[index + 1].sent_start = False
        prev = token.text
    return doc


nlp.add_pipe('my_component', before='parser')


def detokenize(tokens):
    out = []
    for token in tokens:
        if token.original_spelling is not None:
            out.append(token.original_spelling)
        else:
            out.append(token.text)
        if token.space_after:
            out.append(" ")
    return "".join(out)


def sentencizer(text):
    sents = []
    # tokenizer = SoMaJo("en_PTB", xml_sentences="s")
    # sentences = tokenizer.tokenize_text([text])
    # for sentence in sentences:
    #     for token in sentence:
    #         print(token.text)
    doc = nlp(text)
    sent_lst = doc.sents
    for sent in sent_lst:
        sents.append(sent.text)
    return sents


def _check_in_tokenizer(src):
    with tokenizer.as_target_tokenizer():
        labels = tokenizer([src], max_length=102400, padding=False, truncation=True,
                           target_side=True)

    label_splits = []
    label_split = []
    is_a_good_example = True
    modified = False
    for idx, id in enumerate(labels['input_ids'][0]):
        if id != 0 and id != 2:
            label_split.append(id)
        else:
            if idx > 0 and id == 2:
                label_splits.append(label_split.copy())
                label_split = []

    if len(label_splits) != len(src.split('</s><s> ')):
        print('inside bad example')
        import pdb;pdb.set_trace()
        is_a_good_example=False
        return is_a_good_example, modified, None

    modified_sents = []
    for sent_text, s_ids in zip(src.split('</s><s> '), label_splits):
        if len(s_ids) > 2:
            modified_sents.append(sent_text.strip())
        else:
            modified = True
            continue

    modified_src = '</s><s> '.join(modified_sents)

    return is_a_good_example, modified, modified_src


def _mp_sentencizer(param):
    reddit_post = param
    if reddit_post['id'] == 'test-1604':
        reddit_post['document'] = reddit_post['summary']
        reddit_post['summary'] = 'I let a "friend" move into our walk-in closet'

    post = sentencizer(reddit_post['document'])
    src_sents = []
    for i, sent in enumerate(post):
        if len(sent.strip()) > 0 and len(sent.strip().split()) > 2:
            src_sents.append(sent.strip())

    src = '</s><s> '.join(src_sents)

    src = src.strip()

    # check to see if Contextualized tokenizer also can handle the sentences...

    is_a_good_example, modified, new_src = _check_in_tokenizer(src)

    if is_a_good_example and len(src.strip()) > 0:
        while modified:
            print('modified loop')
            is_a_good_example, modified, new_src = _check_in_tokenizer(new_src)
            if not is_a_good_example:
                print(f'bad example after modification {reddit_post["id"]}')
                return reddit_post['id']

        reddit_post['document'] = new_src
        return reddit_post
    else:
        print(f'bad example {reddit_post["id"]}')
        return reddit_post['id']


BASE_RD_DIR = "/home/code-base/user_space/packages/datasets/reddit_tifu-full/"
BASE_WR_DIR = "/home/code-base/user_space/packages/datasets/reddit_tifu_segmented-enhanced/"

if not os.path.exists(BASE_WR_DIR):
    os.makedirs(BASE_WR_DIR)

for set in ["test", "validation", "train"]:
    fW = open(BASE_WR_DIR + set + '.json', mode='w')
    posts = []
    num_lines = sum(1 for line in open(BASE_RD_DIR + set + '.json', 'r'))
    with open(BASE_RD_DIR + set + '.json') as fR:
        for l in tqdm(fR, total=num_lines):
            reddit_post = json.loads(l.strip())
            if reddit_post is not None:
                posts.append(reddit_post)

        pool = Pool(70)

        wr_posts = []
        for f in tqdm(posts, total=len(posts)):
            reddit_post = _mp_sentencizer(f)
            if not isinstance(reddit_post, str):
                wr_posts.append(reddit_post)

        for rp in tqdm(wr_posts, total=len(wr_posts), desc=f'Writing {set}'):
            json.dump(rp, fW)
            fW.write('\n')

    # for reddit_post in tqdm(pool.imap_unordered(_mp_sentencizer, posts), total=len(posts), desc=f'Writing {set} posts'):
        #     if not isinstance(reddit_post, str):
        #         json.dump(reddit_post, fW)
        #         fW.write('\n')
        #     else:
        #         import pdb;pdb.set_trace()
    fW.close()

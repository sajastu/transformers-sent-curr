import json

from somajo import SoMaJo
from tqdm import tqdm

tokenizer = SoMaJo("en_PTB", split_camel_case=True)

class Result():
    def __init__(self, path='', test=''):
        self.path = path

        if len(test) == 0:
            self.summaries = self.read_summaries(self.path)

        else:
            self.summaries = self.read_test_summaries(test)

        self.stat = {
            'avg_tokens': 0,
            'avg_sents': 0
        }


    def read_test_summaries(self, test_path):
        out = []
        with open(test_path) as fR:
            for l in fR:
               out.append(json.loads(l.strip())['summary'])
        return out

    def read_summaries(self, path):
        out = []
        with open(path) as fR:
            for l in fR:
                out.append(l.strip())
        return out

    def _tokenize(self, text):
        sent = []
        tokens = []

        sentences = tokenizer.tokenize_text([text])
        for sentence in sentences:
            for token in sentence:
                # print("{}\t{}\t{}".format(token.text, tokens.token_class, tokens.extra_info))
                tokens.append(token.text)
            # print()

        return {'tokens': tokens, 'sents': sent}

    def compute_tokens(self):
        for j, s in tqdm(enumerate(self.summaries), total=len(self.summaries)):

            ent_stats = self._tokenize(s)

            self.stat['avg_tokens'] += len(ent_stats['tokens'])
            self.stat['avg_sents'] += len(ent_stats['sents'])

        for key, val in self.stat.items():
            self.stat[key] = (float(val) / int((j+1)))

        print(self.stat)

if __name__ == '__main__':
    # r = Result('generated_predictions_lambda9ch24.txt')
    r = Result('generated_predictions_bartSmall.txt')
    r.compute_tokens()
    r = Result('generated_predictions_bartCurr.txt')
    r.compute_tokens()
    r = Result(test='../reddit_tifu/test.json')
    r.compute_tokens()
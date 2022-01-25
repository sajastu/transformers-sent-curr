from datasets import load_dataset
from spacy.lang.en import English
nlp = English()
nlp.add_pipe("sentencizer")


save_path = '/saved_models/bart/bart-cnn/generated_predictions.txt'

raw_datasets = load_dataset(
            'ccdv/cnn_dailymail', "3.0.0"
        )
test_dataset = raw_datasets['test']

references = []

for instance in test_dataset:
    references.append(instance['highlights'])

output_lns = []
for x in open(save_path).readlines():
    output_sents = nlp(x.rstrip())
    output_sents_text = []

    for sent in output_sents:
        import pdb;pdb.set_trace()
        output_sents_text.append(sent.text)



 # = [" . \n".join(.split('. ')) ]
reference_lns = [" . \n".join(x.rstrip().split(' . ')) for x in open(args.reference_path).readlines()][: len(output_lns)]

from datasets import load_dataset
from datasets import load_metric
from rouge_score import rouge_scorer, scoring
ROUGE_KEYS = ["rouge1", "rouge2", "rougeL", "rougeLsum"]

metric = load_metric("rouge")

from spacy.lang.en import English
nlp = English()
nlp.add_pipe("sentencizer")

def calculate_rouge(
    pred_lns,
    tgt_lns,
    use_stemmer=True,
    rouge_keys=ROUGE_KEYS,
    return_precision_and_recall=False,
    bootstrap_aggregation=True,
    newline_sep=True,
):
    """Calculate rouge using rouge_scorer package.

    Args:
        pred_lns: list of summaries generated by model
        tgt_lns: list of groundtruth summaries (e.g. contents of val.target)
        use_stemmer:  Bool indicating whether Porter stemmer should be used to
        strip word suffixes to improve matching.
        rouge_keys:  which metrics to compute, defaults to rouge1, rouge2, rougeL, rougeLsum
        return_precision_and_recall: (False) whether to also return precision and recall.
        bootstrap_aggregation: whether to do the typical bootstrap resampling of scores. Defaults to True, if False
            this function returns a collections.defaultdict[metric: list of values for each observation for each subscore]``
        newline_sep:(default=True) whether to add newline between sentences. This is essential for calculation rougeL
        on multi sentence summaries (CNN/DM dataset).

    Returns:
         Dict[score: value] if aggregate else defaultdict(list) keyed by rouge_keys

    """
    scorer = rouge_scorer.RougeScorer(rouge_keys, use_stemmer=use_stemmer)
    aggregator = scoring.BootstrapAggregator()
    for pred, tgt in zip(tgt_lns, pred_lns):
        # rougeLsum expects "\n" separated sentences within a summary
        # if newline_sep:
        #     pred = add_newline_to_end_of_each_sentence(pred)
        #     tgt = add_newline_to_end_of_each_sentence(tgt)
        scores = scorer.score(pred, tgt)
        aggregator.add_scores(scores)

    if bootstrap_aggregation:
        result = aggregator.aggregate()
        if return_precision_and_recall:
            return extract_rouge_mid_statistics(result)  # here we return dict
        else:
            return {k: round(v.mid.fmeasure * 100, 4) for k, v in result.items()}

    else:
        return aggregator._scores  # here we return defaultdict(list)



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
    for sent in output_sents.sents:
        output_sents_text.append(sent.text)
    output_lns.append(output_sents_text)

reference_lns = []
for x in references:
    output_sents = nlp(x.rstrip())
    reference_sents_text = []
    for sent in output_sents.sents:
        reference_sents_text.append(sent.text)
    reference_lns.append(reference_sents_text)



output_lns = [" . \n".join(x).lower() for x in output_lns]
reference_lns = [" . \n".join(x).lower() for x in reference_lns][: len(output_lns)]
# import pdb;pdb.set_trace()
print(calculate_rouge(output_lns, reference_lns))
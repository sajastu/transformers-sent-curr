from datasets import load_dataset

save_path = '/saved_models/bart/bart-cnn/generated_predictions.txt'

raw_datasets = load_dataset(
            'ccdv/cnn_dailymail', "3.0.0"
        )
test_dataset = raw_datasets['test']

references = []

for instance in test_dataset:
    import pdb;pdb.set_trace()


output_lns = [" . \n".join(x.rstrip().split('. ')) for x in open(save_path).readlines()]
reference_lns = [" . \n".join(x.rstrip().split(' . ')) for x in open(args.reference_path).readlines()][: len(output_lns)]

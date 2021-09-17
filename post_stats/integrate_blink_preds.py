import json

segmented_preds = []
with open('/trainman-mount/trainman-k8s-storage-349d2c46-5192-4e7b-8567-ada9d1d9b2de/saved_models/bart-ext/bart-curr/generated_predictions.txt') as fR:
    for l in fR:
        segmented_preds.append(l.strip())

segmented_ids = []
with open('blink_test_segmented/test.json') as fR:
    for l in fR:
        segmented_ids.append(json.loads(l.strip())['id'])

cases = {}
for seg_id, seg_pred in zip(segmented_ids, segmented_preds):
    case_id = seg_id.split('-')[0]
    if case_id not in cases.keys():
        cases[case_id] = seg_pred
    else:
        cases[case_id] += ' '
        cases[case_id] += seg_pred


with open('blink_test_segmented/final_preds.json', mode='w') as fW:
    for k, v in cases.items():
        json.dump(
            {'file': k,
             'summary': v
             },
            fW
        )
        fW.write('\n')
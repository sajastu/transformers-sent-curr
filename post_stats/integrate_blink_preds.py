import json

segmented_preds = []
with open('/trainman-mount/trainman-k8s-storage-349d2c46-5192-4e7b-8567-ada9d1d9b2de/saved_models/bart-ext/bart-curr/generated_predictions.txt') as fR:
    for l in fR:
        segmented_preds.append(l.strip())

segmented_ids = []
paragraphs = []
with open('blink_test_segmented/test.json') as fR:
    for l in fR:
        segmented_ids.append(json.loads(l.strip())['id'])
        paragraphs.append(json.loads(l.strip())['document'])

cases = {}
cases_par = []
for seg_id, par, seg_pred in zip(segmented_ids, paragraphs, segmented_preds):
    cases_par.append({'segment_id': seg_id, 'paragraph_text': par, 'paragraph_summary': seg_pred})
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

with open('blink_test_segmented/paragraph_summaries_350.json', mode='w') as fW:
    for ent in cases_par:
        json.dump(ent, fW)
        fW.write('\n')
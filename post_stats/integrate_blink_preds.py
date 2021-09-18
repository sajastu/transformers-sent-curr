import json
import subprocess

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
cases_par = {}
for seg_id, par, seg_pred in zip(segmented_ids, paragraphs, segmented_preds):
    case_id = seg_id.split('-')[0]
    if case_id not in cases.keys():
        cases[case_id] = seg_pred
        cases_par[case_id] = [{'segment_id': seg_id, 'paragraph_text': par, 'paragraph_summary': seg_pred}]
    else:
        cases[case_id] += ' '
        cases[case_id] += seg_pred
        cases_par[case_id].append({'segment_id': seg_id, 'paragraph_text': par, 'paragraph_summary': seg_pred})


with open('blink_test_segmented/final_preds.json', mode='w') as fW:
    for k, v in cases.items():
        json.dump(
            {'file': k,
             'summary': v
             },
            fW
        )
        fW.write('\n')
        subprocess.call(['gupload', 'blink_test_segmented/final_preds.json'])

for k, pars in cases_par.items():
    with open(f'blink_test_segmented/blink_summary_{k.replace("blink/", "")}.json', mode='w') as fW:
        for ent in pars:
            json.dump(ent, fW)
            fW.write('\n')
    subprocess.call(['gupload', f'blink_test_segmented/blink_summary_{k.replace("blink/", "")}.json'])

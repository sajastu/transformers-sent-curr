# import json
# import subprocess
#
# segmented_preds = []
# with open('/trainman-mount/trainman-k8s-storage-349d2c46-5192-4e7b-8567-ada9d1d9b2de/saved_models/bart-ext/bart-curr/generated_predictions.txt') as fR:
#     for l in fR:
#         segmented_preds.append(l.strip())
#
#
# METHOD = '300'
# segmented_ids = []
# paragraphs = []
# with open(f'blink_test_segmented/test_{METHOD}.json') as fR:
#     for l in fR:
#         segmented_ids.append(json.loads(l.strip())['id'])
#         paragraphs.append(json.loads(l.strip())['document'])
#
# cases = {}
# cases_par = {}
# for seg_id, par, seg_pred in zip(segmented_ids, paragraphs, segmented_preds):
#     case_id = seg_id.split('-')[0]
#     if case_id not in cases.keys():
#         cases[case_id] = seg_pred
#         cases_par[case_id] = [{'segment_id': seg_id, 'paragraph_text': par, 'paragraph_summary': seg_pred}]
#     else:
#         cases[case_id] += ' '
#         cases[case_id] += seg_pred
#         cases_par[case_id].append({'segment_id': seg_id, 'paragraph_text': par, 'paragraph_summary': seg_pred})
#
#
# with open(f'blink_test_segmented/final_preds_{METHOD}.json', mode='w') as fW:
#     for k, v in cases.items():
#         json.dump(
#             {'file': k,
#              'summary': v
#              },
#             fW
#         )
#         fW.write('\n')
# subprocess.call(['gupload', f'blink_test_segmented/final_preds_{METHOD}.json'])
#
# for k, pars in cases_par.items():
#     with open(f'blink_test_segmented/blink_summary_{k.replace("blink/", "")}_{METHOD}.json', mode='w') as fW:
#         for ent in pars:
#             json.dump(ent, fW)
#             fW.write('\n')
#     subprocess.call(['gupload', f'blink_test_segmented/blink_summary_{k.replace("blink/", "")}_{METHOD}.json'])


############################################################################

import json
import subprocess






all_segmented_ids = []
all_paragraphs = []
with open(f'blink_test_segmented/test_50_m1_all.json') as fR:
    for l in fR:
        all_segmented_ids.append(json.loads(l.strip())['id'])
        all_paragraphs.append(json.loads(l.strip())['document'])


segmented_preds = []
with open('/trainman-mount/trainman-k8s-storage-349d2c46-5192-4e7b-8567-ada9d1d9b2de/saved_models/bart-ext/bart-curr/generated_predictions.txt') as fR:
    for l in fR:
        segmented_preds.append(l.strip())

METHOD = '50_m1_bart'
segmented_ids = []
paragraphs_bart = []
with open(f'blink_test_segmented/test_{METHOD}.json') as fR:
    for l in fR:
        segmented_ids.append(json.loads(l.strip())['id'])
        paragraphs_bart.append(json.loads(l.strip())['document'])

cases = {}
cases_par = {}
for seg_id, par, seg_pred in zip(segmented_ids, paragraphs_bart, segmented_preds):
    case_id = seg_id.split('-')[0]
    if case_id not in cases.keys():
        cases[case_id] = seg_pred
        cases_par[case_id] = [{'segment_id': seg_id, 'paragraph_text': par, 'paragraph_summary': seg_pred}]
    else:
        cases[case_id] += ' '
        cases[case_id] += seg_pred
        cases_par[case_id].append({'segment_id': seg_id, 'paragraph_text': par, 'paragraph_summary': seg_pred})


cases_all = {}

for seg_id, par in zip(all_segmented_ids, all_paragraphs):
    case_id = seg_id.split('-')[0]
    if seg_id in [s['segment_id'] for s in cases_par[case_id]]:
        if case_id in cases_all.keys():
            cases_all[case_id] = [{'segment_id': seg_id, 'paragraph_text': par,
                                       'paragraph_summary': cases_par[case_id][cases_par[case_id].index(seg_id)]}]
        else:
            cases_all[case_id].append({'segment_id': seg_id, 'paragraph_text': par, 'paragraph_summary': cases_par[case_id][cases_par[case_id].index(seg_id)]})
    else:
        if case_id in cases_all.keys():
            cases_all[case_id] = [{'segment_id': seg_id, 'paragraph_text': par,
                                       'paragraph_summary': 'NA'}]
        else:
            cases_all[case_id].append({'segment_id': seg_id, 'paragraph_text': par, 'paragraph_summary': 'NA'})

with open(f'blink_test_segmented/final_preds_{METHOD}.json', mode='w') as fW:
    for k, v in cases.items():
        json.dump(
            {'file': k,
             'summary': v
             },
            fW
        )
        fW.write('\n')
subprocess.call(['gupload', f'blink_test_segmented/final_preds_{METHOD}.json'])

for k, pars in cases_all.items():
    with open(f'blink_test_segmented/blink_summary_{k.replace("blink/", "")}_{METHOD}.json', mode='w') as fW:
        for ent in pars:
            json.dump(ent, fW)
            fW.write('\n')
    subprocess.call(['gupload', f'blink_test_segmented/blink_summary_{k.replace("blink/", "")}_{METHOD}.json'])
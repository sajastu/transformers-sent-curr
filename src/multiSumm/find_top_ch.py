import json

BASE_DIR = '/home/code-base/user_space/trainman-k8s-storage-c91414be-d3d1-431d-a2c8-1d040368c6e8/saved_models/bart-ext/reddit-lr3e5-sentDecoder-superloss-lambda0.5/'

steps_score = {}

with open(BASE_DIR + 'trainer_state.json') as F:

    all_logs = json.load(F)


for a in all_logs['log_history']:
    if 'eval_rougeL' in a.keys():
        steps_score[a['step']] = a['eval_rougeL']
# import pdb;pdb.set_trace()

sorted = sorted(steps_score.items(), key=lambda item: item[1], reverse=True)

for s in sorted:
    print(s)

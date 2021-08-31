import glob
import random
import shutil

from tqdm import tqdm

all_new_files = []
all_data_count = 8676731 + 43821 + 43823

for f in glob.glob("/home/code-base/tldr_dataset/20-21-tldrs/tldr_data_p2/*"):
    all_new_files.append(f)
#
random.seed(8080)
random.shuffle(all_new_files)
all_data_count += len(all_new_files)

train_split_upper = int(0.99 * all_data_count)

should_train_count = int(0.99 * all_data_count) - 8676731
should_val_count = int(0.005 * all_data_count) - 43821
should_test_count = int(0.005 * all_data_count) - 43823

rotation_set = {
    'train': should_train_count,
    'validation': should_val_count,
    'test': should_test_count
}
set = 'train'
import pdb;pdb.set_trace()
for a in tqdm(all_new_files, total=len(all_new_files)):
    shutil.copy(a, f'/home/code-base/tldr_dataset/splits/{set}/')
    rotation_set[set] -= 1
    if rotation_set[set] == 0:
        if set == 'train':
            print(f'{set} files moved..')
            set = 'validation'
        elif set == 'validation':
            print(f'{set} files moved..')
            set = 'test'
        elif set == 'test':
            print(f'{set} files moved..')
            break
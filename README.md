# Text Summarization of Reddit posts using Curriculum Learning

This repository contains the implementation of text summarization of Reddit posts via Curriculum Learning that is applied during the training. 

## DISCLAIMER
This repository is based on (i.e., extended over) ``transformers`` Huggingface. The readme is updated to meet instructions on how running the implemented code.

## Configuration
Before starting to run the code, you need to configure the system. Thesee stages will be done only once. Follow the following steps:
1. Clone the repository:
```angular2html
cd /tmp
git clone  https://sotudehg:8975ac48fe626969c06d0756d571cacd7c9b82db@git.azr.adobeitc.com/sotudehg/transformers-sent-curr.git
```

2. Check to see if you have installed cona (or Anaconda) on your system. If not, follow the step (4); and if so, skip to step (5).
   
3. Make sure you have ``conda`` installed on your local. If it is not installed on your system, run the following, and follow the installation steps:


```angular2html
wget https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh
bash Anaconda3-2021.05-Linux-x86_64.sh
```

Note that you would need to pass the installation steps to install Conda/Anaconda. After installing, you can remove the installer file:

```angular2html
rm Anaconda3-2021.05-Linux-x86_64.sh
```



4. To install the required packages (and all dependencies), run the following command:
```angular2html
conda env create -f environment.yml
conda activate currSumm
```

5. Install the ``transformers`` package by the following command:
```angular2html
mv transformers-sent-curr transformers
cd transformers
pip install -e .
```

6. As the last stage, run the following bash scrip to set up the model and ds path:
```angular2html
source set_path.sh
```

* `wandb` is a visualization toolkit that is also intergrated in this project. Please use the following command to configure it before training: `wandb login`. This will ask your username, enter your username, then pass the access token as instructed.

## Data Preparation
Download the Reddit TIFU dataset as it is provided in the root directoy as ``reddit_tifu.tar`` and then uncopress it useing the following command:
````angular2html
tar -xzf reddit_tifu.tar 
````

This script will uncompress ``reddit_tifu`` dataset to the current directo. You will find the splits within `reddit_tifu/` folder.

## Training

To facilitate the training, we have provided a bash script by which the training will start on BART model. You can easily change the parameters within the bash script.
````angular2html
bash bart_train.sh
````

## Evaluation
To facilitate the training, we have provided a bash script by which the training will start on BART model. You can easily change the parameters within the bash script.
````angular2html
bash bart_eval.sh
````



export DS_BASE_DIR_P=/tmp/transformers/reddit_tifu_enhanced-ext-wRg/
export DS_BASE_DIR_P=reddit_tifu/

export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
export MODEL=bart-ext
export M_ID=reddit-lr3e5-sentDecoder-superloss-lambda0.9
export SAVE_MODEL_DIR=/home/code-base/user_space
#  --model_name_or_path $SAVE_MODEL_DIR/saved_models/$MODEL/$M_ID/checkpoint-20000/\

python -m torch.distributed.launch --nproc_per_node=2 examples/pytorch/summarization/run_summarization.py --task_mode abstractive\
    --model_name_or_path /trainman-mount/trainman-k8s-storage-349d2c46-5192-4e7b-8567-ada9d1d9b2de/saved_models/bart-ext/bart-curr/checkpoint-20000 \
    --do_predict \
    --train_file $DS_BASE_DIR_P/train.json \
    --validation_file $DS_BASE_DIR_P/validation.json \
    --test_file $DS_BASE_DIR_P/test.json \
    --output_dir /trainman-mount/trainman-k8s-storage-349d2c46-5192-4e7b-8567-ada9d1d9b2de/saved_models/bart-ext/bart-curr/checkpoint-20000/ \
    --per_device_train_batch_size=2 \
    --per_device_eval_batch_size=8  \
    --overwrite_output_dir \
    --predict_with_generate \
    --text_column document \
    --summary_column summary
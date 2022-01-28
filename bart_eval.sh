
export DS_BASE_DIR_P=/home/code-base/transformers/blink_test_segmented/

export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
export MODEL=bart-ext
export M_ID=reddit-lr3e5-sentDecoder-superloss-lambda0.9
export SAVE_MODEL_DIR=/home/code-base/user_space
#  --model_name_or_path $SAVE_MODEL_DIR/saved_models/$MODEL/$M_ID/checkpoint-20000/\

#python -m torch.distributed.launch --nproc_per_node=8 examples/pytorch/summarization/run_summarization.py --task_mode abstractive\
CUDA_VISIBLE_DEVICES=0 python examples/pytorch/summarization/run_summarization.py --task_mode abstractive\
    --model_name_or_path /saved_models/bart/bart-cnn-checkpoint-168000/ \
    --do_predict \
    --output_dir /saved_models/bart/bart-cnn/ \
    --per_device_train_batch_size=2 \
    --per_device_eval_batch_size=8  \
    --overwrite_output_dir \
    --predict_with_generate \
    --dataset_name  ccdv/cnn_dailymail \
    --dataset_config "3.0.0" \
    --load_best_model_at_end False

#python post_stats/integrate_blink_preds.py
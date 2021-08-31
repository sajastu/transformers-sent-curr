

de /tmp/
rm -rf transformers
git clone https://sajastu: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@github.com/sajastu/transformers-sent-curr.git
mv transformers-sent-curr/ transformers/
tar -xf reddit_tifu.tar
pip install -e .

source set_path.sh



python -m torch.distributed.launch --nproc_per_node=8 examples/pytorch/summarization/run_summarization.py \
    --task_mode abstractive \
    --model_name_or_path facebook/bart-large \
    --do_train \
    --do_eval \
    --do_predict \
    --output_dir $SAVE_MODEL_DIR/saved_models/$MODEL/$M_ID \
    --per_device_train_batch_size=1 \
    --per_device_eval_batch_size=8  \
    --learning_rate 3e-5 \
    --weight_decay 0.01 \
    --adam_beta2 0.98 \
    --num_train_epochs 8 \
    --overwrite_output_dir \
    --evaluation_strategy steps  --eval_steps 1000 --save_steps 1000 --warmup_steps 10000 --logging_steps 100 \
    --text_column document \
    --summary_column summary \
    --train_file $DS_BASE_DIR/train.json \
    --validation_file $DS_BASE_DIR/validation.json \
    --test_file $DS_BASE_DIR/test.json \
    --predict_with_generate
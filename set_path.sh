
user_space_tr=$(python disk.py)

! ln -sf $user_space_tr /home/code-base/user_space/

for f in /home/code-base/user_space/tr*
do
  export SAVE_MODEL_DIR="${f}"
done

export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
export MODEL=bart-ext
export M_ID=pretrained_rg_largQ
export DS_BASE_DIR=$SAVE_MODEL_DIR/tldrQ/


echo "SAVE_MODEL_DIR is $SAVE_MODEL_DIR"

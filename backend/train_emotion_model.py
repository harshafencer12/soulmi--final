"""
Fine-tune the pretrained FER2013 mini-XCEPTION model on your own labelled
face images (transfer learning), instead of using the generic pretrained
weights as-is.
 
Why fine-tune at all: the pretrained model was trained on the FER2013
dataset (lab photos, mostly Western faces, studio lighting). Fine-tuning
on a smaller set of images that look like your actual users/webcam
conditions usually improves real-world accuracy noticeably.
 
1. Collect data
   Create this folder structure under backend/data/train and
   backend/data/val (an 80/20 split is a reasonable default):
 
       data/train/angry/*.jpg
       data/train/disgust/*.jpg
       data/train/fear/*.jpg
       data/train/happy/*.jpg
       data/train/sad/*.jpg
       data/train/surprise/*.jpg
       data/train/neutral/*.jpg
       data/val/<same 7 folders>/*.jpg
 
   Images can be any size/format — they're resized to 64x64 grayscale
   automatically. A public starting point is the FER2013 dataset on
   Kaggle if you don't have your own labelled faces yet.
 
2. Make sure the base pretrained weights exist:
       python download_pretrained_model.py
 
3. Run this script:
       python train_emotion_model.py --epochs 15 --freeze-base
 
   --freeze-base (recommended for small datasets, <2000 images/class):
       only the last conv block + output layer are trainable, so the
       model keeps everything FER2013 already learned about faces and
       just adapts the final decision boundary to your data.
   Drop --freeze-base once you have a larger dataset (a few thousand
   images per class) to fine-tune the whole network with a low
   learning rate.
 
The result is saved to models/fer2013_mini_XCEPTION_finetuned.hdf5,
which emotion_model.py picks up automatically over the generic weights.
"""
 
import argparse
import os
 
from emotion_model import build_mini_xception, PRETRAINED_WEIGHTS, FINETUNED_WEIGHTS, INPUT_SIZE, EMOTIONS, MODELS_DIR
 
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
 
 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=15)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--freeze-base", action="store_true",
                         help="Only fine-tune the last residual block + output layer.")
    args = parser.parse_args()
 
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    from tensorflow.keras.optimizers import Adam
    from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
 
    train_dir = os.path.join(DATA_DIR, "train")
    val_dir = os.path.join(DATA_DIR, "val")
    if not os.path.isdir(train_dir) or not os.path.isdir(val_dir):
        raise SystemExit(
            f"Expected labelled images under {train_dir} and {val_dir} "
            "(one subfolder per emotion). See the docstring at the top of this file."
        )
 
    if not os.path.exists(PRETRAINED_WEIGHTS):
        raise SystemExit("Run `python download_pretrained_model.py` first.")
 
    os.makedirs(MODELS_DIR, exist_ok=True)
 
    print("Building mini-XCEPTION and loading pretrained FER2013 weights...")
    model = build_mini_xception(input_shape=(*INPUT_SIZE, 1), num_classes=len(EMOTIONS))
    model.load_weights(PRETRAINED_WEIGHTS)
 
    if args.freeze_base:
        # Freeze everything except the last residual module (128-filter block)
        # and the final classification layers, so a small custom dataset can't
        # wreck the general face-expression features already learned.
        freeze_until_found = False
        for layer in model.layers:
            if "separable_conv2d_5" in layer.name or "conv2d_7" in layer.name:
                freeze_until_found = True
            layer.trainable = freeze_until_found
        print("Base layers frozen — fine-tuning only the last block + head.")
    else:
        print("Fine-tuning the entire network with a low learning rate.")
 
    model.compile(
        optimizer=Adam(learning_rate=args.lr),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
 
    # Same [-1, 1] scaling as inference (emotion_model.py) — the base
    # pretrained weights were trained on this range, so fine-tuning needs
    # to match it too.
    def _scale_to_pm1(x):
        return (x - 0.5) * 2.0
 
    train_gen = ImageDataGenerator(
        rescale=1.0 / 255,
        preprocessing_function=_scale_to_pm1,
        rotation_range=10,
        width_shift_range=0.05,
        height_shift_range=0.05,
        zoom_range=0.1,
        horizontal_flip=True,
    ).flow_from_directory(
        train_dir, target_size=INPUT_SIZE, color_mode="grayscale",
        classes=EMOTIONS, class_mode="categorical", batch_size=args.batch_size,
    )
 
    val_gen = ImageDataGenerator(
        rescale=1.0 / 255, preprocessing_function=_scale_to_pm1
    ).flow_from_directory(
        val_dir, target_size=INPUT_SIZE, color_mode="grayscale",
        classes=EMOTIONS, class_mode="categorical", batch_size=args.batch_size,
    )
 
    callbacks = [
        ModelCheckpoint(FINETUNED_WEIGHTS, monitor="val_accuracy",
                         save_best_only=True, save_weights_only=True, verbose=1),
        EarlyStopping(monitor="val_accuracy", patience=4, restore_best_weights=True),
    ]
 
    model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=args.epochs,
        callbacks=callbacks,
    )
 
    print(f"Fine-tuned weights saved to {FINETUNED_WEIGHTS}")
    print("Restart the Flask server (or it'll pick this up on next /api/detect-mood call).")
 
 
if __name__ == "__main__":
    main()
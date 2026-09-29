"""
Evaluate the facial-expression model (accuracy, precision, recall, F1).

Uses whichever weights emotion_model.py would use at runtime (fine-tuned if
present, otherwise the generic pretrained ones), so the numbers you get here
describe exactly the model the website is running.

Expected folder layout (same as train_emotion_model.py), one sub-folder
per emotion, containing labelled face images:

    data/val/angry/*.jpg
    data/val/disgust/*.jpg
    data/val/fear/*.jpg
    data/val/happy/*.jpg
    data/val/sad/*.jpg
    data/val/surprise/*.jpg
    data/val/neutral/*.jpg

Usage (from the backend folder, venv active):

    python evaluate_emotion_model.py                    # evaluates data/val
    python evaluate_emotion_model.py --data-dir data/test
"""

import argparse
import os
import sys

import cv2
import numpy as np

from emotion_model import EMOTIONS, INPUT_SIZE, _get_model, active_model_kind

IMG_EXTS = (".jpg", ".jpeg", ".png", ".bmp")


def load_dataset(data_dir):
    images, labels = [], []
    for idx, emotion in enumerate(EMOTIONS):
        folder = os.path.join(data_dir, emotion)
        if not os.path.isdir(folder):
            print(f"  (skipping missing folder: {folder})")
            continue
        for name in sorted(os.listdir(folder)):
            if not name.lower().endswith(IMG_EXTS):
                continue
            img = cv2.imread(os.path.join(folder, name), cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            img = cv2.resize(img, INPUT_SIZE)
            img = img.astype("float32") / 255.0
            img = (img - 0.5) * 2.0  # same [-1, 1] scaling as inference/training
            images.append(img[..., np.newaxis])
            labels.append(idx)
    return np.array(images, dtype="float32"), np.array(labels)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", default=os.path.join(os.path.dirname(__file__), "data", "val"))
    parser.add_argument("--batch-size", type=int, default=64)
    args = parser.parse_args()

    if not os.path.isdir(args.data_dir):
        sys.exit(
            f"Folder not found: {args.data_dir}\n"
            "Create labelled test images under <data-dir>/<emotion>/*.jpg "
            "(see the docstring at the top of this file)."
        )

    print(f"Loading images from {args.data_dir} ...")
    X, y_true = load_dataset(args.data_dir)
    if len(X) == 0:
        sys.exit("No images found. Check the folder layout.")
    print(f"Loaded {len(X)} images.")

    model = _get_model()
    print(f"Evaluating the {active_model_kind()} model ...")
    probs = model.predict(X, batch_size=args.batch_size, verbose=0)
    y_pred = np.argmax(probs, axis=1)

    n = len(EMOTIONS)
    cm = np.zeros((n, n), dtype=int)
    for t, p in zip(y_true, y_pred):
        cm[t, p] += 1

    tp = np.diag(cm).astype(float)
    support = cm.sum(axis=1).astype(float)
    predicted = cm.sum(axis=0).astype(float)
    precision = np.divide(tp, predicted, out=np.zeros(n), where=predicted > 0)
    recall = np.divide(tp, support, out=np.zeros(n), where=support > 0)
    denom = precision + recall
    f1 = np.divide(2 * precision * recall, denom, out=np.zeros(n), where=denom > 0)

    accuracy = tp.sum() / cm.sum()
    present = support > 0
    macro_f1 = f1[present].mean()
    weighted_f1 = (f1 * support).sum() / support.sum()

    print("\n" + "=" * 62)
    print(f"{'Class':<10}{'Precision':>11}{'Recall':>10}{'F1-score':>11}{'Support':>10}")
    print("-" * 62)
    for i, name in enumerate(EMOTIONS):
        print(f"{name:<10}{precision[i]:>11.3f}{recall[i]:>10.3f}{f1[i]:>11.3f}{int(support[i]):>10}")
    print("-" * 62)
    print(f"Accuracy      : {accuracy:.4f}  ({accuracy * 100:.2f}%)")
    print(f"Macro F1      : {macro_f1:.4f}")
    print(f"Weighted F1   : {weighted_f1:.4f}")
    print("=" * 62)

    print("\nConfusion matrix (rows = true, columns = predicted):")
    print(" " * 10 + "".join(f"{e[:5]:>7}" for e in EMOTIONS))
    for i, name in enumerate(EMOTIONS):
        print(f"{name:<10}" + "".join(f"{v:>7}" for v in cm[i]))


if __name__ == "__main__":
    main()
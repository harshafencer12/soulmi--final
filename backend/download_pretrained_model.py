"""
One-time setup: downloads the public pretrained FER2013 mini-XCEPTION
weights (MIT licensed, from oarriaga/face_classification on GitHub) so
/api/detect-mood works out of the box, before you've fine-tuned anything.

Run once from the backend folder:
    python download_pretrained_model.py
"""

import os
import urllib.request

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
DEST = os.path.join(MODELS_DIR, "fer2013_mini_XCEPTION_pretrained.hdf5")

URL = (
    "https://raw.githubusercontent.com/oarriaga/face_classification/"
    "master/trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5"
)


def main():
    os.makedirs(MODELS_DIR, exist_ok=True)
    if os.path.exists(DEST):
        print(f"Already downloaded: {DEST}")
        return

    print(f"Downloading pretrained emotion model weights to {DEST} ...")
    urllib.request.urlretrieve(URL, DEST)
    print("Done. /api/detect-mood is ready to use.")
    print("To specialise the model further, see train_emotion_model.py.")


if __name__ == "__main__":
    main()

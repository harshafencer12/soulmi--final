"""
Facial expression -> mood detection.
 
Base architecture: mini-XCEPTION, trained on FER2013 (7 classes).
Pretrained weights come from the well-known open-source project
oarriaga/face_classification (MIT licensed). Run
`python download_pretrained_model.py` once to fetch them.
 
To specialise the model instead of using the generic pretrained weights,
run `train_emotion_model.py` (see that file for the transfer-learning
recipe). If a fine-tuned weights file is present, it is loaded instead
of the generic pretrained one automatically.
"""
 
import os
import numpy as np
import cv2
 
MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
PRETRAINED_WEIGHTS = os.path.join(MODELS_DIR, "fer2013_mini_XCEPTION_pretrained.hdf5")
FINETUNED_WEIGHTS = os.path.join(MODELS_DIR, "fer2013_mini_XCEPTION_finetuned.hdf5")
 
EMOTIONS = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]
INPUT_SIZE = (64, 64)
 
_face_cascade = None
_model = None
_active_weights_path = None
 
 
def build_mini_xception(input_shape=(64, 64, 1), num_classes=7):
    """Recreates the mini-XCEPTION architecture so pretrained/fine-tuned
    .hdf5 weight files (which store weights only, not the graph) can be
    loaded into it. Keep this in sync with train_emotion_model.py."""
    from tensorflow.keras.layers import (
        Input, Conv2D, BatchNormalization, Activation, SeparableConv2D,
        MaxPooling2D, GlobalAveragePooling2D, Add
    )
    from tensorflow.keras.regularizers import l2
    from tensorflow.keras.models import Model
 
    regularization = l2(0.01)
    img_input = Input(input_shape)
 
    x = Conv2D(8, (3, 3), strides=(1, 1), kernel_regularizer=regularization,
               use_bias=False)(img_input)
    x = BatchNormalization()(x)
    x = Activation("relu")(x)
    x = Conv2D(8, (3, 3), strides=(1, 1), kernel_regularizer=regularization,
               use_bias=False)(x)
    x = BatchNormalization()(x)
    x = Activation("relu")(x)
 
    for num_filters in (16, 32, 64, 128):
        residual = Conv2D(num_filters, (1, 1), strides=(2, 2), padding="same",
                           use_bias=False)(x)
        residual = BatchNormalization()(residual)
 
        x = SeparableConv2D(num_filters, (3, 3), padding="same",
                             depthwise_regularizer=regularization,
                             pointwise_regularizer=regularization, use_bias=False)(x)
        x = BatchNormalization()(x)
        x = Activation("relu")(x)
        x = SeparableConv2D(num_filters, (3, 3), padding="same",
                             depthwise_regularizer=regularization,
                             pointwise_regularizer=regularization, use_bias=False)(x)
        x = BatchNormalization()(x)
 
        x = MaxPooling2D((3, 3), strides=(2, 2), padding="same")(x)
        x = Add()([x, residual])
 
    x = Conv2D(num_classes, (3, 3), padding="same")(x)
    x = GlobalAveragePooling2D()(x)
    output = Activation("softmax", name="predictions")(x)
 
    return Model(img_input, output)
 
 
def _get_face_cascade():
    global _face_cascade
    if _face_cascade is None:
        cascade_path = os.path.join(
            os.path.dirname(cv2.__file__), "data", "haarcascade_frontalface_default.xml"
        )
        _face_cascade = cv2.CascadeClassifier(cascade_path)
    return _face_cascade
 
 
def _get_model():
    """Lazily builds the model and loads the best available weights,
    preferring a fine-tuned checkpoint over the generic pretrained one."""
    global _model, _active_weights_path
 
    weights_path = FINETUNED_WEIGHTS if os.path.exists(FINETUNED_WEIGHTS) else PRETRAINED_WEIGHTS
 
    if _model is not None and _active_weights_path == weights_path:
        return _model
 
    if not os.path.exists(weights_path):
        raise FileNotFoundError(
            "No emotion model weights found. Run "
            "`python download_pretrained_model.py` in the backend folder first."
        )
 
    model = build_mini_xception(input_shape=(*INPUT_SIZE, 1), num_classes=len(EMOTIONS))
    model.load_weights(weights_path)
 
    _model = model
    _active_weights_path = weights_path
    return _model
 
 
def active_model_kind():
    return "fine-tuned" if os.path.exists(FINETUNED_WEIGHTS) else "pretrained"
 
 
def detect_faces_and_emotions(bgr_image, max_faces=1):
    """bgr_image: numpy array (as read by cv2.imread / cv2.imdecode).
    Returns a list of {box, emotion, confidence, scores} dicts, largest face first."""
    model = _get_model()
    gray = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
 
    faces = _get_face_cascade().detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(48, 48)
    )
    if len(faces) == 0:
        return []
 
    # Largest faces first
    faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)[:max_faces]
 
    results = []
    for (x, y, w, h) in faces:
        face_roi = gray[y:y + h, x:x + w]
        face_roi = cv2.resize(face_roi, INPUT_SIZE)
        face_roi = face_roi.astype("float32") / 255.0
        face_roi = (face_roi - 0.5) * 2.0  # scale to [-1, 1] — matches how the pretrained/fine-tuned weights were trained
        face_roi = np.expand_dims(face_roi, axis=(0, -1))  # (1, 64, 64, 1)
 
        scores = model.predict(face_roi, verbose=0)[0]
        idx = int(np.argmax(scores))
 
        results.append({
            "box": {"x": int(x), "y": int(y), "w": int(w), "h": int(h)},
            "emotion": EMOTIONS[idx],
            "confidence": float(scores[idx]),
            "scores": {EMOTIONS[i]: float(scores[i]) for i in range(len(EMOTIONS))},
        })
 
    return results
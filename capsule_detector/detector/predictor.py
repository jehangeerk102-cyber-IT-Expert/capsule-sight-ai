from pathlib import Path
import numpy as np
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / 'models' / 'model.h5'
if not MODEL_PATH.exists():
    MODEL_PATH = BASE_DIR / 'model.h5'
CLASS_NAMES = ['Ulcer', 'Normal', 'AVM']
IMG_SIZE = (224, 224)
_model = None


def get_model():
    global _model
    if _model is None:
        try:
            import tensorflow as tf
        except ImportError as exc:
            raise RuntimeError('TensorFlow is not installed. Run: pip install -r requirements.txt') from exc
        _model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    return _model


def predict_image(image_file):
    model = get_model()
    # Always trust the serialized model signature over notebook defaults.
    # The supplied H5 currently expects (None, 128, 128, 3).
    shape = model.input_shape
    if isinstance(shape, list):
        shape = shape[0]
    height = int(shape[1]) if shape[1] else IMG_SIZE[0]
    width = int(shape[2]) if shape[2] else IMG_SIZE[1]
    channels = int(shape[3]) if len(shape) > 3 and shape[3] else 3
    image = Image.open(image_file).convert('RGB')
    if channels == 1:
        image = image.convert('L')
    image = image.resize((width, height))
    array = np.asarray(image, dtype=np.float32)
    if channels == 1:
        array = np.expand_dims(array, axis=-1)
    batch = np.expand_dims(array, axis=0)
    raw = np.asarray(model.predict(batch, verbose=0)).squeeze()
    if raw.ndim == 0:
        raw = np.array([float(raw)])
    if raw.size == 1:
        score = float(raw.item())
        probabilities = np.array([1 - score, score])
        labels = ['Normal', 'Abnormal']
    else:
        labels = CLASS_NAMES[:raw.size]
        if np.any(raw < 0) or not np.isclose(raw.sum(), 1.0, atol=0.05):
            exp = np.exp(raw - np.max(raw))
            probabilities = exp / exp.sum()
        else:
            probabilities = raw / raw.sum()
    index = int(np.argmax(probabilities))
    return {
        'label': labels[index],
        'confidence': round(float(probabilities[index]) * 100, 2),
        'probabilities': [
            {'label': label, 'value': round(float(prob) * 100, 2)}
            for label, prob in zip(labels, probabilities)
        ],
    }

# CapsuleSight Django App

CapsuleSight is a professional Django interface for the supplied VGG19 capsule-endoscopy classifier. The notebook defines the classes **AVM**, **Normal**, and **Ulcer**. The saved H5 model signature is authoritative at runtime and currently expects **128 × 128 × 3** inputs; the app reads that signature automatically.

## Project layout

```text
config/             project configuration namespace
 detector/          Django app, views and prediction service
 media/             uploaded images at runtime
 ml/                machine-learning extension namespace
 models/model.h5    canonical trained model
 scripts/           utility scripts
 capsule_detector/  Django settings, URLs and WSGI
 manage.py          Django entry point
 model.h5           compatibility copy for simple deployments
 requirements.txt   Python dependencies
 setup.sh           Linux/macOS setup
 setup_windows.bat  Windows setup
```

## Local setup

Linux/macOS:

```bash
cd capsule_detector
bash setup.sh
source .venv/bin/activate
python manage.py runserver
```

Windows:

```bat
cd capsule_detector
setup_windows.bat
.venv\Scripts\activate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. Upload a JPG, PNG, BMP, or WEBP frame up to 10 MB. TensorFlow loads the H5 model lazily on the first prediction, so the server can start before the model is loaded.

## Important model note

The canonical model is stored at `models/model.h5`; the root `model.h5` and `model/capsul_model.h5` copies are retained for compatibility with common deployment layouts. The notebook indicates a three-class softmax-style classifier. The prediction service also handles a single-output binary model defensively. If the saved model contains its own preprocessing layer, it is preserved; otherwise the service passes resized RGB pixels directly.

## Production checklist

Set a strong `SECRET_KEY`, set `DEBUG=False`, restrict `ALLOWED_HOSTS`, serve static/media through a proper web server or object storage, and add authentication/rate limiting before public deployment. This is a research and decision-support interface, not a medical diagnosis system; all results should be reviewed by a qualified clinician.

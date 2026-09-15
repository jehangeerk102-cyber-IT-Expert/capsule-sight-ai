# CapsuleSight

### AI-assisted capsule endoscopy image screening

CapsuleSight is a **Django + TensorFlow/Keras** web application for reviewing capsule-endoscopy frames with an image-classification model. Upload an endoscopy image, run inference, and view the predicted class together with its confidence distribution in a clean clinical-style interface.

> **Important:** CapsuleSight is a research and decision-support tool. It is **not** a medical device and must not be used as a standalone diagnostic system. Every result should be reviewed by a qualified healthcare professional.

---

## Overview

The application currently supports three model classes:

| Class | Meaning |
| --- | --- |
| `Ulcer` | Image classified as showing an ulcer-like finding |
| `Normal` | Image classified as normal |
| `AVM` | Image classified as an arteriovenous malformation-like finding |

The model is loaded lazily when the first prediction is requested. The prediction service reads the serialized model input shape at runtime, converts the uploaded image to RGB, resizes it as required, and returns the top class with a probability breakdown.

## Key features

- Modern, responsive clinical-style upload dashboard.

- TensorFlow/Keras H5 model integration.

- Lazy model loading for faster server startup.

- Automatic image resizing based on the saved model signature.

- Support for `JPG`, `JPEG`, `PNG`, `BMP`, and `WEBP` images.

- Upload validation with a **10 MB** size limit.

- Prediction confidence and per-class probability display.

- SQLite database for simple local development.

- Separate Linux/macOS and Windows setup scripts.

- Development media serving through Django.

---

## Application workflow

```
User selects image
        │
        ▼
Django validates extension and file size
        │
        ▼
Image is saved to media/uploads/
        │
        ▼
TensorFlow loads models/model.h5
        │
        ▼
Image is converted, resized, and classified
        │
        ▼
Label, confidence, and probabilities are rendered
```

---

## Tech stack

- **Backend:** Python, Django 5

- **Machine learning:** TensorFlow/Keras

- **Image processing:** Pillow, NumPy

- **Model format:** H5 / Keras saved model

- **Database:** SQLite for development

- **Frontend:** Django templates, HTML, CSS, JavaScript

- **Deployment entry point:** WSGI

---

## Project structure

```
capsule_detector/
├── capsule_detector/
│   ├── settings.py              # Django configuration
│   ├── urls.py                  # Application routes
│   └── wsgi.py                  # WSGI entry point
├── detector/
│   ├── predictor.py             # Model loading and image inference
│   ├── views.py                 # Upload and prediction views
│   └── apps.py
├── templates/
│   └── detector/
│       └── home.html            # Main application screen
├── static/
│   └── detector/                # Frontend static assets
├── models/
│   └── model.h5                # Primary trained model
├── media/                       # Runtime-uploaded images
├── ml/                          # Machine-learning namespace
├── config/                      # Project namespace
├── scripts/                     # Utility scripts
├── manage.py                    # Django CLI entry point
├── requirements.txt             # Python dependencies
├── setup.sh                     # Linux/macOS setup
├── setup_windows.bat            # Windows setup
├── .env.example                 # Environment configuration example
└── README.md
```

---

## Requirements

Install the following before starting:

- Python **3.10 or newer**

- `pip`

- Python virtual-environment support

- A system capable of running TensorFlow

- At least 2 GB of free disk space for dependencies and the model

Dependencies are defined in `requirements.txt`:

```
Django>=5.0,<6.0
Pillow>=10.0
numpy>=1.26
h5py>=3.10
tensorflow>=2.15
```

---

## Quick start

### 1. Enter the project directory

```bash
cd capsule_detector
```

### 2. Linux/macOS setup

```bash
bash setup.sh
source .venv/bin/activate
```

If required, make the script executable first:

```bash
chmod +x setup.sh
```

### 3. Windows setup

Open Command Prompt in the project directory:

```
setup_windows.bat
.venv\Scripts\activate
```

### 4. Start the development server

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

### 5. Start on a custom port

```bash
python manage.py runserver 8080
```

The application will then be available at `http://127.0.0.1:8080/`.

---

## Manual installation

Use this method if you do not want to use the setup scripts.

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Windows

```
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## Model setup

The preferred model location is:

```
models/model.h5
```

The predictor also supports a fallback model at:

```
model.h5
```

The model is loaded with:

```python
tf.keras.models.load_model(MODEL_PATH, compile=False  )
```

At inference time, the service:

1. Opens the uploaded file with Pillow.

1. Converts it to RGB, or grayscale if the model expects one channel.

1. Reads the model input dimensions.

1. Resizes the image to those dimensions.

1. Creates a batch dimension.

1. Runs the TensorFlow prediction.

1. Converts the output into class probabilities.

1. Returns the predicted label and confidence percentage.

The code handles both multi-class outputs and a single-output binary model defensively.

---

## Routes and upload contract

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/` | Displays the CapsuleSight interface |
| `POST` | `/predict/` | Validates the image and runs prediction |

The upload field must be named `image`.

### Example with cURL

```bash
curl -X POST \
  -F "image=@/absolute/path/to/endoscopy-image.jpg" \
  http://127.0.0.1:8000/predict/
```

The current implementation renders the result into the HTML page. It does not expose a separate JSON API endpoint.

### Validation rules

- Accepted extensions: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.webp`

- Maximum file size: `10 MB`

- Uploaded files are saved under `media/uploads/`

- Invalid files receive a user-facing error message

---

## Configuration

The repository includes an example environment file:

```
DJANGO_SECRET_KEY=replace-with-a-long-random-secret
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

For production, connect these values to Django settings through a secure environment-variable mechanism. Do not commit real secrets to Git.

The current development defaults include:

- SQLite database: `db.sqlite3`

- Media root: `media/`

- Static URL: `/static/`

- Media URL: `/media/`

- Time zone: `Asia/Karachi`

---

## Common commands

```bash
# Apply database migrations
python manage.py migrate

# Check the Django project
python manage.py check

# Start the development server
python manage.py runserver

# Run on all interfaces for local-network testing
python manage.py runserver 0.0.0.0:8000

# Collect static files for deployment
python manage.py collectstatic
```

---

## Troubleshooting

### `TensorFlow is not installed`

Activate the virtual environment and install dependencies again:

```bash
pip install -r requirements.txt
```

### `Model file not found`

Confirm that one of the following exists:

```
models/model.h5
model.h5
```

### First prediction is slow

This is expected. TensorFlow and the H5 model are loaded lazily on the first prediction. Subsequent predictions in the same process normally start faster.

### Port already in use

Use another port:

```bash
python manage.py runserver 8080
```

### Upload rejected

Check that the image is one of the supported formats and smaller than 10 MB.

### Migration error

Run:

```bash
python manage.py migrate
```

---

## Production hardening checklist

Before making this application publicly accessible:

- [ ] Replace the default Django `SECRET_KEY`.

- [ ] Set `DEBUG = False`.

- [ ] Restrict `ALLOWED_HOSTS` to trusted domains.

- [ ] Use HTTPS.

- [ ] Configure secure CSRF and session-cookie settings.

- [ ] Serve static and media files with a proper web server or object storage.

- [ ] Add authentication and rate limiting.

- [ ] Define a retention and deletion policy for uploaded medical images.

- [ ] Restrict access to patient-related data.

- [ ] Log failures without storing unnecessary sensitive information.

- [ ] Validate the model against representative, properly governed data.

- [ ] Add automated tests for upload validation and prediction responses.

Example WSGI command:

```bash
gunicorn capsule_detector.wsgi:application
```

Install Gunicorn if necessary:

```bash
pip install gunicorn
```

---

## Responsible use

AI predictions can be uncertain, biased, or incorrect. Confidence scores should not be interpreted as clinical certainty. The application should be used only within an appropriate clinical or research workflow, with qualified human oversight and suitable data-protection controls.

---

## License

Add the appropriate software, model, and dataset licenses before distributing this project. Confirm that the training data, trained weights, and any third-party assets permit the intended use.

---

## Maintainer notes

When changing the model classes, update the class mapping in:

```
detector/predictor.py
```

When changing upload limits or supported formats, update the validation constants in:

```
detector/views.py
```

Keep the README synchronized with any changes to the model path, input shape, routes, deployment process, or privacy behavior.

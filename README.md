# AI Age Detection

An AI-based age detection system that predicts a person's age from an image using a deep learning model (ResNet18) served through a Flask web application.

## Features

- Upload an image and get a predicted age instantly through a simple web interface
- ResNet18-based CNN model trained for age classification/regression
- Batch testing support for evaluating multiple images at once
- Training/evaluation notebook included with accuracy, loss, and confusion matrix visualizations

## Project Structure

```
AI_Age_Detection_Project/
├── app.py                          # Flask app entry point
├── model.py                        # Model architecture definition
├── predict.py                      # Inference / prediction logic
├── requirements.txt                # Python dependencies
├── models/
│   ├── age_classifier.pth
│   └── resnet18_age_detection.pth
├── static/                         # CSS, JS, and static assets
├── templates/                      # HTML templates for the web app
├── tests/
│   ├── batch_test_recursive.py
│   └── test_image/
├── Code File/
│   └── AI_Age_Detection_Project_structured.ipynb   # Training/eval notebook
└── Results/
    ├── Accuracy curve.png
    ├── Loss curve.png
    ├── Accuracy And Loss Curve.png
    ├── Confussion Matrix.png
    ├── Classified Score.png
    └── Scores.png
```

## Installation

1. Clone the repository
   ```bash
   git clone <your-repo-url>
   cd AI_Age_Detection_Project
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Run the web app
```bash
python app.py
```
Then open `http://localhost:5000` in your browser, upload an image, and view the predicted age.

### Run predictions from script
```bash
python predict.py --image path/to/image.jpg
```

### Run batch tests
```bash
python tests/batch_test_recursive.py
```

## Model

- **Architecture:** ResNet18 (transfer learning / fine-tuned)
- **Weights:** stored in `models/resnet18_age_detection.pth` and `models/age_classifier.pth`
- **Training details:** see `Code File/AI_Age_Detection_Project_structured.ipynb` for the full training pipeline, hyperparameters, and evaluation.

## Results

Training and evaluation plots are available in the `Results/` folder, including:
- Accuracy and loss curves
- Confusion matrix
- Classification scores

## Requirements

See `requirements.txt` for the full list of dependencies (e.g. PyTorch, Flask, NumPy, Pillow).

## License

Specify your license here (e.g. MIT, Apache 2.0).

## Acknowledgements

Add any datasets, papers, or resources you referenced while building this project.

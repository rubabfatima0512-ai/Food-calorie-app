# Computer Vision-Based Food Recognition and Calorie Estimation System

A college final-year project that identifies food items from images using a
Vision Transformer (ViT) trained on the Food-101 dataset (101 food classes),
then estimates calories and nutritional information from a SQLite database.

## Project Structure

| File | Proposal Module |
|---|---|
| `app.py` | Module 1 — User Interface (Streamlit web app) |
| `food_classifier.py` | Modules 2 & 3 — Image preprocessing (OpenCV) + Food recognition (ViT model) |
| `calorie_estimator.py` | Modules 4 & 5 — Calorie estimation + nutritional info (SQLite) |
| `setup_database.py` | Builds `nutrition.db` (101 foods: calories, protein, carbs, fat) |
| `demo_cli.py` | Command-line demo version |
| `model/` | Pre-trained ViT weights (optional — auto-downloads if missing) |
| `test_images/` | Sample food images for testing |

## Setup

Requires Python 3.10+.

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install transformers pillow opencv-python streamlit numpy pandas
```

Then build the nutrition database (one time):

```bash
python3 setup_database.py
```

## Running the Demo

**Web app (recommended for the project demo):**
```bash
streamlit run app.py
```
Open the URL shown (usually http://localhost:8501), upload a food photo,
adjust portion size, and see the predicted dish, calories and nutrition.

**Command line:**
```bash
python3 demo_cli.py test_images/pizza.jpg --portions 1.5
```

## How It Works

1. **Image acquisition & preprocessing** — the image is read with OpenCV,
   converted BGR→RGB and resized to 224×224.
2. **Food recognition** — a Vision Transformer (`nateraw/vit-base-food101`,
   fine-tuned on Food-101) outputs probabilities over 101 food classes;
   the top-3 predictions are shown with confidence scores.
3. **Calorie estimation** — the top prediction is looked up in the SQLite
   `nutrition.db` and scaled by the selected portion size.
4. **Results dashboard** — Streamlit displays the dish name, estimated
   calories, protein, carbohydrates and fat.

## Notes

- Calorie/nutrition values are **estimates per typical serving**, meant for
  awareness and tracking — the same approach used by commercial food apps.
- On first run without the `model/` folder, weights download automatically
  from Hugging Face (~340 MB, one time).
- Tested on pizza, hamburger and sushi images — all classified correctly
  as the top-1 prediction.

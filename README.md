# Area Type Determination - Development Process

This repository documents the step-by-step process of building an educational machine learning project for classifying place names as business or residential areas.

## Step 1: Data Generation
- **generate_random_points.py**: Defines Winnipeg bounding box (south=49.7136, north=49.9925, west=-97.3499, east=-96.9497). Generates 10 random lat/lon points using `random.uniform`, saves coordinates to `random_points.txt` in CSV format.
- Later modified to generate 100 points for expanded dataset, with output to `test_random_points.txt` for independent testing.

## Step 2: Geocoding
- **reverse_geocode_points.py**: Reads coordinates from `random_points.txt`, sends each to Nominatim reverse geocoding API to get full address details (name, display_name, address type, etc.). Saves results as JSON array to `geocoded_points.json`.
- Includes 1-second delays between requests to respect API rate limits. Modified version processes `test_random_points.txt` and outputs to `test_geocoded_points.json` for unbiased evaluation.

## Step 3: Labeling
- **classify_areas.py**: Loads `geocoded_points.json`, inspects `address.addresstype` field. Assigns "residential" for "building" or "road" types, "business" for "amenity". Adds `area_type` field to each point.
- **add_mcdonalds.py**: Searches Nominatim for "McDonald's Winnipeg" (limit 10), reverse geocodes each, adds to dataset with "business" label. Later extended to add 50 Tim Hortons locations to address class imbalance (originally 91 residential vs 19 business).

## Step 4: Model Training
- **train_model.py**: Loads labeled dataset, uses `display_name` as text feature (fallback to `name`). Applies TF-IDF vectorization (max 1000 features) to convert text to numerical vectors. Trains Logistic Regression classifier on 80% of data.
- Evaluates on 20% holdout set, prints classification report. Saves trained model to `area_classifier.pkl` and vectorizer to `vectorizer.pkl` for later use. Retrained after adding Tim Hortons to improve performance on business class.

## Step 5: Testing and Evaluation
- **test_model.py**: Loads saved model and vectorizer, defines test texts (mix of known business/residential), vectorizes and predicts. Prints results to verify functionality.
- **predict_test.py**: Loads model, applies to entire `test_geocoded_points.json`, adds `predicted_area_type` field, saves to `test_predictions.json`. Counts residential/business predictions.
- **evaluate_test.py**: Loads predictions, re-applies heuristic labeling to test data for ground truth, compares with predictions, calculates accuracy (82% achieved).
- **show_business.py**: Loads dataset, filters points where `area_type` == "business", prints details (lat/lon, name, display_name, type) for inspection.

## Additional Scripts
- **get_area.py**: Example script to query Overpass API for detailed area data around a point.

## Final Dataset
- `geocoded_points.json`: 160 points (91 residential, 69 business).
- `test_geocoded_points.json`: 100 points for testing.
- Model achieves 82% accuracy on test set, better after balancing data.

## How to Reproduce
1. Run `python generate_random_points.py` (for training data).
2. Run `python reverse_geocode_points.py`.
3. Run `python classify_areas.py`.
4. Run `python add_mcdonalds.py` (for Tim Hortons).
5. Run `python train_model.py`.
6. For testing: `python generate_random_points.py` (modify for test), `python reverse_geocode_points.py`, `python predict_test.py`, `python evaluate_test.py`.

This process demonstrates data collection, preprocessing, labeling, training, and evaluation in ML for text classification.

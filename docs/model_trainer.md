# Model Trainer Pipeline

The Model Trainer pipeline is responsible for:

1. Training multiple machine learning models
2. Performing hyperparameter tuning
3. Evaluating model performance
4. Selecting the best model
5. Calculating classification metrics
6. Combining preprocessor and trained model
7. Saving the final prediction pipeline
8. Creating model trainer artifacts

---

# Model Trainer Related Files

| File | Purpose |
|------|----------|
| `model_trainer.py` | Contains the complete model training pipeline logic |
| `config_entity.py` | Contains configuration classes for model trainer |
| `artifact_entity.py` | Contains artifact classes used in model training |
| `training_pipeline_constants.py` | Contains reusable model trainer constants |
| `ml_metric_utils.py` | Contains classification metric utility functions |
| `ml_model_utils.py` | Contains prediction model wrapper class |
| `main_utils.py` | Contains utility functions like save/load/evaluate |

---

# Model Trainer Constants

Model trainer constants are stored inside:

```txt
src/constants/training_pipeline_constants.py
````

Most model trainer constants start with:

```python
MODEL_TRAINER_
```

Example:

```python
MODEL_TRAINER_DIR_NAME = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_FILE_PATH = "model.pkl"

MODEL_TRAINER_EXPECTED_ACCURACY_SCORE = 0.6
MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD = 0.05
```

These constants help avoid hardcoded values inside the project.

---

# ModelTrainerConfig

The `ModelTrainerConfig` class is stored inside:

```txt
src/entity/config_entity.py
```

This class dynamically creates all model trainer related runtime paths.

It creates paths for:

* model trainer directory
* trained model directory
* final model path

---

# Generated Artifact Structure

```txt
Artifacts/
└── 27_05_2026_03_10_45/
    └── model_trainer/
        └── trained_model/
            └── model.pkl
```

---

# ModelTrainerArtifact

The model trainer outputs are stored using:

```txt
src/entity/artifact_entity.py
```

Example:

```python
from dataclasses import dataclass

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str
    train_metric_artifact: ClassificationMetricArtifact
    test_metric_artifact: ClassificationMetricArtifact
```

This artifact contains:

* trained model path
* train metrics
* test metrics

These outputs are later used by prediction pipelines and deployment systems.

---

# ClassificationMetricArtifact

Classification metrics are stored using:

```python
from dataclasses import dataclass

@dataclass
class ClassificationMetricArtifact:
    f1_score: float
    precision_score: float
    recall_score: float
```

This artifact stores:

* F1 Score
* Precision Score
* Recall Score

for both train and test datasets.

---

# PredictionModel

The prediction model wrapper is stored inside:

```txt
src/utils/ml_model_utils.py
```

Example:

```python
class PredictionModel:
    def __init__(self, preprocessor, model):
        self.preprocessor = preprocessor
        self.model = model
```

This class combines:

* preprocessing object
* trained model

into a single prediction pipeline.

---

# Why PredictionModel is Needed

Machine learning models require transformed input data.

During prediction:

1. Raw data is received
2. Preprocessor transforms data
3. Model performs prediction

Without saving the preprocessor together with the model:

* predictions may fail
* feature mismatch can occur
* production inference becomes inconsistent

The wrapper ensures consistent preprocessing during inference.

---

# Runtime Flow

## Step 1 — Model Trainer Starts

`ModelTrainer` receives:

* `ModelTrainerConfig`
* `DataTransformationArtifact`

---

## Step 2 — Load Transformed Arrays

Train and test numpy arrays are loaded.

Example:

```python
train_arr = load_numpy_array_data(train_file_path)
test_arr = load_numpy_array_data(test_file_path)
```

---

## Step 3 — Split Features and Target

Arrays are divided into:

* X_train
* y_train
* X_test
* y_test

---

## Step 4 — Train Multiple Models

Multiple classification models are initialized.

Example:

```python
models = {
    "Decision Tree": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier(),
    "Gradient Boosting": GradientBoostingClassifier(),
    "Logistic Regression": LogisticRegression(),
    "AdaBoost": AdaBoostClassifier(),
}
```

---

## Step 5 — Hyperparameter Tuning

`GridSearchCV` is used for hyperparameter tuning.

Example:

```python
grid_search = GridSearchCV(
    model,
    param,
    cv=3,
    verbose=2,
    n_jobs=-1
)
```

This helps find the best parameters for each model.

---

# Step 6 — Model Evaluation

All models are evaluated on test data.

The evaluation utility returns:

* model scores
* trained models

Example:

```python
model_report, trained_models = evaluate_model(...)
```

---

# Step 7 — Best Model Selection

Best model is selected using:

```python
best_model_name = max(model_report, key=model_report.get)
```

The corresponding trained model becomes the final selected model.

---

# Step 8 — Calculate Classification Metrics

Predictions are generated on:

* training dataset
* testing dataset

Metrics calculated:

* F1 Score
* Precision Score
* Recall Score

using:

```python
get_classification_score()
```

---

# Step 9 — Load Preprocessor

Previously saved preprocessing object is loaded.

Example:

```python
preprocessor = load_object(...)
```

---

# Step 10 — Create Prediction Pipeline

The preprocessor and trained model are combined.

Example:

```python
prediction_model = PredictionModel(
    preprocessor=preprocessor,
    model=best_model
)
```

---

# Step 11 — Save Final Model

Final prediction pipeline is saved as:

```txt
model.pkl
```

inside:

```txt
Artifacts/<timestamp>/model_trainer/trained_model/
```

---

# Purpose of Model Trainer Pipeline

The purpose of the model trainer pipeline is to:

* train multiple ML models
* perform hyperparameter tuning
* evaluate model performance
* select best model
* calculate classification metrics
* create reusable prediction pipeline
* save trained models
* maintain reproducible ML experiments
* prepare model for deployment and prediction

```
```

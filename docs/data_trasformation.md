# Data Transformation Pipeline

The Data Transformation pipeline is responsible for:

1. Reading validated datasets
2. Separating input and target features
3. Handling missing values
4. Applying preprocessing transformations
5. Converting datasets into NumPy arrays
6. Saving transformed datasets and preprocessing objects

---

# Data Transformation Related Files

| File                             | Purpose                                                          |
| -------------------------------- | ---------------------------------------------------------------- |
| `data_transformation.py`         | Contains the main data transformation pipeline logic             |
| `config_entity.py`               | Contains configuration classes for transformation paths          |
| `artifact_entity.py`             | Contains artifact classes for transformation outputs             |
| `training_pipeline_constants.py` | Stores reusable transformation-related constants                 |
| `utils.py`                       | Contains utility functions for saving/loading arrays and objects |

---

# Data Transformation Constants

Data transformation related constants are stored inside:

```txt
src/constants/training_pipeline_constants.py
```

Most transformation constants start with:

```python
DATA_TRANSFORMATION_
```

Example:

```python
DATA_TRANSFORMATION_DIR_NAME = "data_transformation"

DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR = "transformed"

DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR = "transformed_object"

DATA_TRANSFORMATION_TRAIN_FILE_PATH = "train.npy"

DATA_TRANSFORMATION_TEST_FILE_PATH = "test.npy"
```

These constants help avoid hardcoded values inside the project.

---

# DataTransformationConfig

The `DataTransformationConfig` class is stored inside:

```txt
src/entity/config_entity.py
```

This class dynamically creates all transformation-related runtime paths.

It creates paths for:

* transformed train dataset
* transformed test dataset
* preprocessing object

---

# Generated Artifact Structure

```txt
Artifacts/
│
└── 27_05_2026_01_01_21/
    │
    └── data_transformation/
        │
        ├── transformed/
        │   ├── train.npy
        │   └── test.npy
        │
        └── transformed_object/
            └── preprocessor.pkl
```

---

# DataTransformationArtifact

The transformation outputs are stored using:

```txt
src/entity/artifact_entity.py
```

Example:

```python
from dataclasses import dataclass

@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str
```

This artifact contains:

* transformed preprocessing object path
* transformed training array path
* transformed testing array path

These outputs are later used by the model training pipeline.

---

# Input Dataset

The transformation pipeline uses validated datasets generated from the data validation stage.

Input files:

```txt
validated/train.csv
validated/test.csv
```

These files are read using:

```python
pd.read_csv()
```

---

# Target Column Separation

The pipeline separates:

* independent features (`X`)
* target column (`y`)

Target column:

```python
TARGET_COLUMN = "Result"
```

Example:

```python
X_train_df = train_df.drop(columns=TARGET_COLUMN, axis=1)
y_train_df = train_df[TARGET_COLUMN]
```

---

# Data Preprocessing

The transformation pipeline creates a preprocessing pipeline using:

```python
KNNImputer
```

from:

```python
sklearn.impute
```

The preprocessing object is wrapped using:

```python
Pipeline()
```

Example:

```python
preprocessor = Pipeline(
    steps=[
        ("imputer", imputer)
    ]
)
```

---

# KNNImputer

The `KNNImputer` is used to handle missing values.

Example configuration:

```python
DATA_TRANSFORMATION_IMPUTER_PARAMS = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform"
}
```

The imputer replaces missing values using nearest neighboring samples.

---

# Transformation Process

## Training Dataset

The preprocessing object is fitted and transformed using:

```python
X_train_arr = preprocessor.fit_transform(X_train_df)
```

---

## Testing Dataset

The same fitted preprocessor is applied using:

```python
X_test_arr = preprocessor.transform(X_test_df)
```

This prevents data leakage from the test dataset.

---

# Combining Features and Target

After preprocessing:

* transformed features
* target column

are combined into a single NumPy array.

Example:

```python
train_arr = np.column_stack(
    (
        X_train_arr,
        y_train_df.to_numpy()
    )
)
```

---

# Saving Transformed Arrays

The transformed datasets are stored as:

```txt
train.npy
test.npy
```

using:

```python
np.save()
```

Example utility:

```python
save_numpy_array_data()
```

These arrays are later used during model training.

---

# Saving Preprocessing Object

The preprocessing object is saved using:

```python
dill.dump()
```

Example:

```python
save_object(
    file_path=preprocessor_path,
    obj=preprocessor
)
```

The saved preprocessing object ensures the same transformations are applied during inference.

---

# Runtime Flow

## Step 1 — Pipeline Starts

`TrainingPipelineConfig` creates the main artifact folder.

Example:

```txt
Artifacts/27_05_2026_01_01_21/
```

---

## Step 2 — Data Transformation Starts

`DataTransformationConfig` creates transformation-related directories.

Example:

```txt
Artifacts/27_05_2026_01_01_21/data_transformation/
```

---

## Step 3 — Read Validated Datasets

Validated train and test datasets are loaded into pandas DataFrames.

Example:

```python
train_df = pd.read_csv(valid_train_file_path)
test_df = pd.read_csv(valid_test_file_path)
```

---

## Step 4 — Separate Features and Target

The target column is separated from independent features.

Example:

```python
X_train_df = train_df.drop(columns=TARGET_COLUMN)
y_train_df = train_df[TARGET_COLUMN]
```

---

## Step 5 — Apply Preprocessing

The preprocessing pipeline applies:

* missing value handling
* feature transformation

using:

```python
KNNImputer
```

---

## Step 6 — Convert to NumPy Arrays

Processed datasets are converted into NumPy arrays.

Example:

```python
np.column_stack()
```

---

## Step 7 — Save Arrays and Preprocessor

The pipeline saves:

* transformed train array
* transformed test array
* preprocessing object

inside the transformation artifact directory.

---

# Purpose of Data Transformation

The purpose of the data transformation pipeline is to:

* preprocess validated datasets
* handle missing values
* separate features and target columns
* create reusable preprocessing pipelines
* convert datasets into model-ready NumPy arrays
* save reusable preprocessing objects
* prepare clean datasets for model training
* maintain reproducible ML workflows


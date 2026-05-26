# Data Validation Pipeline

The Data Validation pipeline is responsible for:

1. Validating dataset structure
2. Checking required numerical columns
3. Detecting dataset drift
4. Separating valid and invalid datasets
5. Generating drift reports
6. Preparing clean datasets for downstream pipeline stages

---

# Data Validation Related Files

| File                             | Purpose                                             |
| -------------------------------- | --------------------------------------------------- |
| `data_validation.py`             | Contains the main data validation pipeline logic    |
| `config_entity.py`               | Contains configuration classes for validation paths |
| `artifact_entity.py`             | Contains artifact classes for validation outputs    |
| `training_pipeline_constants.py` | Stores reusable validation-related constants        |
| `schema.yaml`                    | Defines expected columns and numerical features     |

---

# Data Validation Constants

Data validation related constants are stored inside:

```txt
src/constants/training_pipeline_constants.py
```

Most validation constants start with:

```python
DATA_VALIDATION_
```

Example:

```python
DATA_VALIDATION_VALID_DIR = "validated"
DATA_VALIDATION_INVALID_DIR = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME = "report.yaml"
```

These constants help avoid hardcoded values across the project.

---

# DataValidationConfig

The `DataValidationConfig` class is stored inside:

```txt
src/entity/config_entity.py
```

This class dynamically creates all validation-related runtime paths.

It creates paths for:

* validated datasets
* invalid datasets
* drift report file

---

# TrainingPipelineConfig

The `TrainingPipelineConfig` class creates the main timestamped artifact directory.

Example:

```txt
Artifacts/26_05_2026_10_30_45/
```

This helps:

* separate different runs
* avoid overwriting files
* maintain pipeline history

---

# Generated Artifact Structure

```txt
Artifacts/
│
└── 26_05_2026_10_30_45/
    │
    └── data_validation/
        │
        ├── validated/
        │   ├── train.csv
        │   └── test.csv
        │
        ├── invalid/
        │   ├── train.csv
        │   └── test.csv
        │
        └── drift_report/
            └── report.yaml
```

---

# DataValidationArtifact

The validation outputs are stored using:

```txt
src/entity/artifact_entity.py
```

Example:

```python
from dataclasses import dataclass

@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str
```

This artifact contains:

* validation status
* validated train dataset path
* validated test dataset path
* invalid train dataset path
* invalid test dataset path
* drift report path

These outputs are later used by downstream pipeline components.

---

# Schema Validation

The validation pipeline reads schema information from:

```txt
data_schema/schema.yaml
```

The schema contains:

* expected dataset columns
* required numerical columns

Example:

```yaml
columns:
  having_IP_Address: int
  URL_Length: int

numerical_columns:
  - having_IP_Address
  - URL_Length
```

The schema acts as the blueprint for validating incoming datasets.

---

# Dataset Drift Detection

Dataset drift detection is performed using:

```python
ks_2samp()
```

from:

```python
scipy.stats
```

The pipeline compares:

* training dataset distribution
* testing dataset distribution

for every column.

---

# Drift Threshold

Default threshold:

```python
threshold = 0.05
```

Logic:

* `p_value >= 0.05`
  → No drift detected

* `p_value < 0.05`
  → Drift detected

---

# Drift Report Generation

The pipeline generates a YAML drift report inside:

```txt
drift_report/report.yaml
```

Example report:

```yaml
having_IP_Address:
    p_value: 0.72
    drift_status: false

URL_Length:
    p_value: 0.01
    drift_status: true
```

This report helps monitor feature distribution changes between datasets.

---

# Runtime Flow

## Step 1 — Pipeline Starts

`TrainingPipelineConfig` creates the main artifact folder.

Example:

```txt
Artifacts/26_05_2026_10_30_45/
```

---

## Step 2 — Data Validation Starts

`DataValidationConfig` creates validation-related directories.

Example:

```txt
Artifacts/26_05_2026_10_30_45/data_validation/
```

---

## Step 3 — Read Train and Test Datasets

Datasets generated during ingestion are loaded into pandas DataFrames.

Example:

```python
train_dataframe = pd.read_csv(train_file_path)
test_dataframe = pd.read_csv(test_file_path)
```

---

## Step 4 — Validate Number of Columns

The pipeline checks whether datasets contain the expected number of columns defined in the schema.

Validation includes:

* train dataset
* test dataset

---

## Step 5 — Validate Numerical Columns

The pipeline verifies whether all required numerical columns exist.

If numerical columns are missing:

* validation fails
* exception is raised

---

## Step 6 — Detect Dataset Drift

The pipeline compares train and test dataset distributions using:

```python
ks_2samp()
```

for every feature column.

A drift report is generated automatically.

---

## Step 7 — Save Valid or Invalid Datasets

### If No Drift Detected

Datasets are stored inside:

```txt
validated/
```

Example:

```txt
validated/train.csv
validated/test.csv
```

---

### If Drift Detected

Datasets are stored inside:

```txt
invalid/
```

Example:

```txt
invalid/train.csv
invalid/test.csv
```

---

# Validation Status Logic

Validation status is created using:

```python
validation_status = not drift_detected
```

Meaning:

* `True` → Dataset is valid
* `False` → Drift detected

---

# Purpose of Data Validation

The purpose of the data validation pipeline is to:

* validate dataset structure
* verify required features
* detect dataset drift
* generate drift reports
* separate valid and invalid datasets
* improve data reliability
* prevent corrupted data from entering training pipelines
* maintain reproducible ML workflows

Based on your validation implementation file 

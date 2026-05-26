# Data Ingestion Pipeline

The Data Ingestion pipeline is responsible for:

1. Fetching data from MongoDB
2. Converting data into DataFrame format
3. Storing raw data
4. Splitting train and test datasets
5. Saving datasets into artifact directories

---

# Data Ingestion Related Files
| File | Purpose |
|------|----------|
| `data_ingestion.py` | Contains the main data ingestion pipeline logic |
| `config_entity.py` | Contains configuration classes for different pipeline components |
| `artifact_entity.py` | Contains artifact classes used to store outputs of pipeline stages |
| `training_pipeline_constants.py` | Contains reusable constants used across the training pipeline |


---

# Data Ingestion Constants

Data ingestion related constants are stored inside:

```txt
src/constants/training_pipeline_constants.py
```

Most ingestion constants start with:

```python
DATA_INGESTION_
```

Example:

```python
DATA_INGESTION_FEATURE_STORE_DIR = "feature_store"
DATA_INGESTION_INGESTED_DIR = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO = 0.2
```

These constants help avoid hardcoded values inside the project.

---

# DataIngestionConfig

The `DataIngestionConfig` class is stored inside:

```txt
src/entity/config_entity.py
```

This class dynamically creates all ingestion-related runtime paths.

It creates paths for:

- feature store directory
- raw dataset
- train dataset
- test dataset

---

# TrainingPipelineConfig

The `TrainingPipelineConfig` class creates the main timestamped artifact directory.

Example:

```txt
Artifacts/26_05_2026_10_30_45/
```

This helps:

- separate different runs
- avoid overwriting files
- maintain pipeline history

---

# Generated Artifact Structure

```txt
Artifacts/
│
└── 26_05_2026_10_30_45/
    │
    └── data_ingestion/
        │
        ├── feature_store/
        │   └── rawPhishingData.csv
        │
        └── ingested/
            ├── train.csv
            └── test.csv
```

---

# DataIngestionArtifact

The ingestion outputs are stored using:

```txt
src/entity/artifact_entity.py
```

Example:

```python
from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file_path:str
    test_file_path:str
```

This artifact constaine paths for:

- train dataset path
- test dataset path

These outputs are later used by the next pipeline component.

---

# Runtime Flow

## Step 1 — Pipeline Starts

`TrainingPipelineConfig` creates the main artifact folder.

Example:

```txt
Artifacts/26_05_2026_10_30_45/
```

---

## Step 2 — Data Ingestion Starts

`DataIngestionConfig` creates ingestion-related directories.

Example:

```txt
Artifacts/26_05_2026_10_30_45/data_ingestion/
```

---

## Step 3 — Fetch Data from MongoDB

Data is fetched from MongoDB collection and converted into a pandas DataFrame.

---

## Step 4 — Store Raw Data

Raw extracted data is stored inside:

```txt
feature_store/rawPhishingData.csv
```
This file acts as a backup copy of the original extracted dataset before train-test splitting.

---

## Step 5 — Train-Test Split

Dataset is split using:

```python
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO = 0.2
```

Meaning:

- 80% training data
- 20% testing data

---

## Step 6 — Save Final Datasets

Final datasets are stored as:

```txt
train.csv
test.csv
```

inside the `ingested/` directory.

---

# Purpose of Data Ingestion

The purpose of the data ingestion pipeline is to:

- fetch data from source systems
- store raw datasets
- split datasets into training and testing files
- create reusable artifact paths
- organize pipeline outputs
- prepare datasets for downstream pipeline components
- maintain reproducible pipeline executions
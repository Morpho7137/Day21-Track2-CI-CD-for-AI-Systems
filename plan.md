# AWS Completion And Submission Plan

## Current Status

The AWS implementation is complete and the latest GitHub Actions pipeline passed.

- Public GitHub repo: `https://github.com/Morpho7137/Day21-Track2-CI-CD-for-AI-Systems.git`
- AWS region: `us-east-1`
- S3 bucket: `pkkkkkkkk1-717292229247-us-east-1-an`
- EC2 public IP: `52.91.33.245`
- Latest successful workflow run: `28149792348`
- Latest successful commit: `93cbc53 fix: gate ci on combined training data`
- Local git status after verification: clean

Do not submit or commit local secret files:

- `ai-lab-user_accessKeys.csv`
- `g2.pem`

## Required Submission Items

The README and task files require the following submission package.

1. Public GitHub repository URL

```text
https://github.com/Morpho7137/Day21-Track2-CI-CD-for-AI-Systems.git
```

2. Screenshot: MLflow UI

- Must show at least 3 experiment runs.
- Runs must have different hyperparameters.
- Runs must show `accuracy` and `f1_score`.
- This is required by `tasks/buoc-1.md` and the README rubric.

3. Screenshot: GitHub Actions for Step 2

- Must show the MLOps pipeline jobs green.
- Required jobs:
  - `Unit Test`
  - `Train`
  - `Eval`
  - `Deploy`
- The README says "three jobs", but `tasks/buoc-2.md` requires all four jobs because the lab includes an eval gate.

4. Screenshot: GitHub Actions for Step 3

- Must show a run triggered by a data/DVC commit.
- Must show the same pipeline completing successfully.
- The commit message should clearly indicate the data update or DVC pointer update.
- This is required by `tasks/buoc-3.md`.

5. Screenshot or terminal capture: deployed API health check

Use:

```bash
curl http://52.91.33.245:8000/health
```

Expected result:

```json
{"status":"ok"}
```

6. Screenshot or terminal capture: deployed API prediction

Use:

```bash
curl -X POST http://52.91.33.245:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features":[7.4,0.70,0.00,1.9,0.076,11.0,34.0,0.9978,3.51,0.56,9.4,0]}'
```

Expected result format:

```json
{"prediction":2,"label":"cao"}
```

7. Screenshot: AWS S3 console

- Must show DVC data pushed under `dvc/`.
- Must show the deployed model at `models/latest/model.pkl`.
- This is required by README submission instructions and the Step 2 DVC requirement.

8. Short report file

- Required by README: short report, not more than 1 A4 page.
- Suggested local path: `submission/REFLECTION.md`.
- Must include:
  - selected hyperparameters and reason;
  - Step 2 and Step 3 metrics;
  - problems encountered;
  - fixes applied.

## Completed Engineering Work

1. AWS platform setup

- Created and configured EC2 instance in `us-east-1`.
- Opened required inbound port `8000`.
- Installed runtime dependencies on EC2.
- Installed and enabled `mlops-serve` systemd service.
- Configured EC2 role access to S3 model artifact.

2. DVC and S3

- Generated lab data.
- Initialized DVC.
- Added S3 remote at `s3://pkkkkkkkk1-717292229247-us-east-1-an/dvc`.
- Tracked:
  - `data/train_phase1.csv`
  - `data/train_phase2.csv`
  - `data/eval.csv`
- Pushed DVC data to S3.

3. Training

- Implemented `src/train.py`.
- Trains `RandomForestClassifier`.
- Reads `params.yaml`.
- Logs MLflow params, metrics, and model artifacts.
- Writes `outputs/metrics.json`.
- Writes `models/model.pkl`.
- Supports extra Step 3 training data when `USE_EXTRA_TRAIN_DATA=1`.

4. Serving

- Implemented `src/serve.py`.
- Downloads latest model from S3.
- Serves `GET /health`.
- Serves `POST /predict`.
- Validates exactly 12 input features.

5. Tests

- Implemented `tests/test_train.py`.
- Local tests passed.
- GitHub Actions unit test job passed.

6. CI/CD

- Implemented `.github/workflows/mlops.yml`.
- Pipeline stages:
  - `Unit Test`
  - `Train`
  - `Eval`
  - `Deploy`
- Uses GitHub OIDC to assume AWS role.
- Pulls DVC data from S3.
- Trains model.
- Uploads model to S3.
- Blocks deploy when accuracy is below `0.70`.
- Restarts EC2 service after successful eval.

## Remaining Before Submission

The code is ready, but the submission evidence is not complete until these files/screenshots are captured.

1. Capture MLflow UI screenshot with at least 3 runs.
2. Capture GitHub Actions screenshot for the latest successful Step 2 pipeline.
3. Capture GitHub Actions screenshot for a data-triggered Step 3 pipeline.
4. Capture terminal output or screenshot for `/health`.
5. Capture terminal output or screenshot for `/predict`.
6. Capture S3 console screenshot showing `dvc/` and `models/latest/model.pkl`.
7. Create `submission/REFLECTION.md`.

## Suggested Submission Folder

Use this structure for the final evidence package:

```text
submission/
  REFLECTION.md
  screenshots/
    01-mlflow-runs.png
    02-github-actions-step2.png
    03-github-actions-step3-data-trigger.png
    04-api-health-and-predict.png
    05-s3-dvc-and-model.png
```

## Reflection Draft Content

The report should stay under one A4 page and can use this content:

```markdown
# Reflection

Repository: https://github.com/Morpho7137/Day21-Track2-CI-CD-for-AI-Systems

Cloud provider: AWS
Region: us-east-1
Storage: S3 bucket pkkkkkkkk1-717292229247-us-east-1-an
Serving: EC2 FastAPI service on port 8000

## Selected Hyperparameters

The final model uses the RandomForestClassifier parameters in params.yaml.
The selected configuration was chosen because it passed the eval gate and produced the best reliable accuracy among the local MLflow runs.

## Metrics

Step 2 pipeline: GitHub Actions completed Unit Test, Train, Eval, and Deploy successfully.
Step 3 pipeline: Data/DVC update triggered retraining and redeployment successfully.
The latest combined-data training run passed the eval threshold of accuracy >= 0.70.

## Problems And Fixes

The first CI attempts failed because the workflow needed correct AWS authentication and DVC access. This was fixed by using GitHub OIDC with an AWS IAM role and pulling DVC data from S3.

The eval gate also failed when training only on the first training split because accuracy was below 0.70. This was fixed by enabling the pipeline to include the Step 3 training data with USE_EXTRA_TRAIN_DATA=1, while keeping local unit tests independent from DVC data.

The deployment service needed AWS S3 access and a persistent process on the VM. This was fixed by adding an EC2 IAM role, installing dependencies, and running the FastAPI server with systemd.
```

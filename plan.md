# AWS Completion Plan

## Summary

Complete the Day21 MLOps CI/CD lab on AWS using:

- Region: `us-east-1`
- S3 bucket: `pkkkkkkkk1-717292229247-us-east-1-an`
- Local AWS access key CSV: `ai-lab-user_accessKeys.csv`
- EC2 SSH key file: `g2.pem`
- GitHub repo target: `https://github.com/Morpho7137/Day21-Track2-CI-CD-for-AI-Systems.git`
- Storage: S3 for DVC data and trained model artifacts
- Serving: EC2 running FastAPI through a `systemd` service
- CI/CD: GitHub Actions test, train, eval gate, and deploy jobs

The access key CSV is for local setup and GitHub Actions secrets only. It must never be committed.

## Inputs Still Needed

- Confirmation that the IAM key has permission to use S3 and, if Codex should create EC2 directly, EC2 permissions.

## Platform Setup

1. Configure AWS credentials locally from `ai-lab-user_accessKeys.csv` for `us-east-1`.
2. Verify access to the S3 bucket `pkkkkkkkk1-717292229247-us-east-1-an`.
3. Create or confirm an EC2 Ubuntu instance in `us-east-1` using the key pair that matches `g2.pem`.
4. Open inbound TCP port `8000` on the EC2 security group.
5. Install Python runtime dependencies on EC2:
   - `fastapi`
   - `uvicorn`
   - `scikit-learn`
   - `joblib`
   - `boto3`
6. Create a `systemd` service named `mlops-serve` with:
   - `S3_BUCKET=pkkkkkkkk1-717292229247-us-east-1-an`
   - `AWS_DEFAULT_REGION=us-east-1`
   - `ExecStart=/usr/bin/python3 /home/ubuntu/src/serve.py`

## Repository Changes

1. Use `.venv` for all local Python installs.
2. Update `requirements.txt`:
   - Replace `dvc[gs]==3.50.1` with `dvc[s3]==3.50.1`
   - Replace `google-cloud-storage==2.16.0` with `boto3`
3. Implement `src/train.py`:
   - Read training and eval CSV files.
   - Train `RandomForestClassifier` using `params.yaml`.
   - Log params and metrics to MLflow.
   - Write `outputs/metrics.json`.
   - Save `models/model.pkl`.
4. Implement `tests/test_train.py`:
   - Generate synthetic Wine Quality schema data.
   - Verify `train()` returns a float in `[0, 1]`.
   - Verify metrics and model files are created.
5. Implement `src/serve.py` for AWS:
   - Download `models/latest/model.pkl` from S3 with `boto3`.
   - Provide `GET /health`.
   - Provide `POST /predict`.
   - Validate exactly 12 input features.
6. Complete `.github/workflows/mlops.yml`:
   - Run unit tests.
   - Authenticate to AWS using GitHub Secrets.
   - Run `dvc pull`.
   - Train model.
   - Read accuracy from `outputs/metrics.json`.
   - Upload model to `s3://pkkkkkkkk1-717292229247-us-east-1-an/models/latest/model.pkl`.
   - Block deploy if accuracy is below `0.70`.
   - SSH into EC2, restart `mlops-serve`, and verify `/health`.
7. Keep `ai-lab-user_accessKeys.csv` ignored by git.

## DVC Setup

1. Generate data with `python generate_data.py`.
2. Initialize DVC with `dvc init`.
3. Add S3 remote:

```bash
dvc remote add -d myremote s3://pkkkkkkkk1-717292229247-us-east-1-an/dvc
```

4. Track data files:

```bash
dvc add data/train_phase1.csv
dvc add data/eval.csv
dvc add data/train_phase2.csv
```

5. Commit DVC metadata and pointer files, not raw CSV data.
6. Push data to S3 with `dvc push`.

## GitHub Secrets

Create these repository secrets:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION` with value `us-east-1`
- `S3_BUCKET` with value `pkkkkkkkk1-717292229247-us-east-1-an`
- `VM_HOST`
- `VM_USER`, usually `ubuntu`
- `VM_SSH_KEY`

## Local Validation

1. Create and activate `.venv`.
2. Install dependencies with `pip install -r requirements.txt`.
3. Run `python generate_data.py`.
4. Run at least three MLflow experiments with different `params.yaml` values.
5. Select the best hyperparameters and leave them in `params.yaml`.
6. Run `pytest tests/ -v`.
7. Run `python src/train.py`.
8. Confirm:
   - `outputs/metrics.json` exists.
   - `models/model.pkl` exists.
   - MLflow UI shows at least three runs.

## CI/CD Validation

1. Push code and DVC pointer files to the public GitHub repo on branch `main`.
2. Confirm GitHub Actions jobs pass:
   - Unit Test
   - Train
   - Eval
   - Deploy
3. Confirm EC2 endpoint:

```bash
curl http://<EC2_PUBLIC_IP>:8000/health
```

4. Confirm prediction endpoint:

```bash
curl -X POST http://<EC2_PUBLIC_IP>:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features":[7.4,0.70,0.00,1.9,0.076,11.0,34.0,0.9978,3.51,0.56,9.4,0]}'
```

## Continuous Retraining

1. Run `python add_new_data.py`.
2. Run `dvc add data/train_phase1.csv`.
3. Commit only `data/train_phase1.csv.dvc`.
4. Run `dvc push`.
5. Push the git commit to `main`.
6. Confirm the full pipeline retrains and redeploys automatically.

## Submission Evidence

- Public GitHub repo URL.
- MLflow UI screenshot showing at least three runs.
- GitHub Actions screenshot showing all jobs green for Step 2.
- GitHub Actions screenshot showing retraining triggered by a data commit for Step 3.
- S3 screenshot showing DVC data under `dvc/` and model under `models/latest/model.pkl`.
- EC2 `/health` and `/predict` outputs.
- Short reflection in `submission/REFLECTION.md` with selected hyperparameters, Step 2 and Step 3 metrics, problems encountered, and fixes.

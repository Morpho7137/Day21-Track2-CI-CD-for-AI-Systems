# Reflection

Repository: https://github.com/Morpho7137/Day21-Track2-CI-CD-for-AI-Systems

Cloud provider: AWS
Region: `us-east-1`
Storage: `s3://pkkkkkkkk1-717292229247-us-east-1-an`
Serving: EC2 FastAPI service on port `8000`

## Selected Hyperparameters

The final training configuration uses `RandomForestClassifier` with the values in `params.yaml`:

- `n_estimators: 800`
- `max_depth: null`
- `min_samples_split: 2`

This configuration was selected because it was the best local baseline before the Step 3 data update and remained compatible with the CI eval gate after combining the extra training data.

## Metrics

Step 2 pipeline:

- GitHub Actions completed `Unit Test`, `Train`, `Eval`, and `Deploy` successfully.
- The final successful Step 2 run is `93cbc5326d266b408970482ad88c9d25008b5b24`.

Step 3 pipeline:

- The data-triggered push commit `ed6fa4309bfd6744e07138553413cca90d8f8986` completed successfully in GitHub Actions.
- The workflow retrained and redeployed the model after the DVC data update.
- The eval gate passed with the combined training data flow.

Local MLflow experiments:

- Run 1: `accuracy = 0.5640`, `f1_score = 0.5534`
- Run 2: `accuracy = 0.6480`, `f1_score = 0.6464`
- Run 3: `accuracy = 0.6700`, `f1_score = 0.6684`

## Problems And Fixes

The first CI attempts failed because AWS authentication and remote data access were not configured correctly. That was fixed by using GitHub OIDC for AWS access, setting the correct S3 bucket, and configuring DVC to pull from the S3 remote.

The eval gate also failed when the model trained only on the initial training split because accuracy stayed below `0.70`. That was fixed by allowing the pipeline to include the Step 3 training data through `USE_EXTRA_TRAIN_DATA=1` during the CI training job.

The deployment service required a persistent process on the EC2 instance and read access to the model artifact in S3. That was fixed by installing the runtime dependencies on EC2, attaching the IAM role, and running the FastAPI app as a `systemd` service.

## Submission Evidence

- MLflow UI screenshot with three runs
- GitHub Actions screenshot for Step 2
- GitHub Actions screenshot for Step 3 data-triggered run
- Terminal output for `/health` and `/predict`
- S3 console screenshot


import mlflow
import mlflow.sklearn
import pandas as pd
import yaml
import json
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

EVAL_THRESHOLD = 0.70


def train(
    params: dict,
    data_path: str = "data/train_phase1.csv",
    eval_path: str = "data/eval.csv",
) -> float:
    """
    Huan luyen mo hinh va ghi nhan ket qua vao MLflow.

    Tham so:
        params     : dict chua cac sieu tham so cho RandomForestClassifier.
        data_path  : duong dan den file du lieu huan luyen.
        eval_path  : duong dan den file du lieu danh gia.

    Tra ve:
        accuracy (float): do chinh xac tren tap danh gia.
    """

    df_train = pd.read_csv(data_path)
    extra_train_path = "data/train_phase2.csv"
    use_extra_train_data = os.getenv("USE_EXTRA_TRAIN_DATA") == "1"
    if use_extra_train_data and os.path.exists(extra_train_path):
        df_extra = pd.read_csv(extra_train_path)
        df_train = pd.concat([df_train, df_extra], ignore_index=True)
    df_eval = pd.read_csv(eval_path)

    X_train = df_train.drop(columns=["target"])
    y_train = df_train["target"]
    X_eval = df_eval.drop(columns=["target"])
    y_eval = df_eval["target"]

    with mlflow.start_run():
        mlflow.log_params(params)

        model = RandomForestClassifier(
            n_estimators=int(params.get("n_estimators", 100)),
            max_depth=params.get("max_depth"),
            min_samples_split=int(params.get("min_samples_split", 2)),
            random_state=42,
        )
        model.fit(X_train, y_train)

        preds = model.predict(X_eval)
        acc = accuracy_score(y_eval, preds)
        f1 = f1_score(y_eval, preds, average="weighted")

        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score", f1)
        mlflow.sklearn.log_model(model, "model")

        print(f"Accuracy: {acc:.4f} | F1: {f1:.4f}")

        os.makedirs("outputs", exist_ok=True)
        with open("outputs/metrics.json", "w", encoding="utf-8") as f:
            json.dump({"accuracy": acc, "f1_score": f1}, f)

        os.makedirs("models", exist_ok=True)
        joblib.dump(model, "models/model.pkl")

    return acc


if __name__ == "__main__":
    with open("params.yaml") as f:
        params = yaml.safe_load(f)
    train(params)

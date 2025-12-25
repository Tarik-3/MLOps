import os
import argparse
import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib
import json

def main(train_folder, model_output, metrics_output):
    train_file = os.path.join(train_folder, "train.csv")
    df = pd.read_csv(train_file)
    X = df[["feature1", "feature2"]]
    y = df["label"]
    model = LogisticRegression(max_iter=200)
    model.fit(X, y)
    os.makedirs(model_output, exist_ok=True)
    model_path = os.path.join(model_output, "model.joblib")
    joblib.dump(model, model_path)
    metrics = {"train_samples": len(df)}
    with open(metrics_output, "w") as f:
        json.dump(metrics, f)
    print(f"Saved model to {model_path}")

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("--train", required=True)
    p.add_argument("--model_output", required=True)
    p.add_argument("--metrics", required=True)
    args = p.parse_args()
    main(args.train, args.model_output, args.metrics)

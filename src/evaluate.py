import os
import argparse
import pandas as pd
import joblib
import json
from sklearn.metrics import accuracy_score

def main(model_folder, test_folder, report_path):
    model_file = os.path.join(model_folder, "model.joblib")
    model = joblib.load(model_file)
    test_file = os.path.join(test_folder, "test.csv")
    df = pd.read_csv(test_file)
    X = df[["feature1", "feature2"]]
    y = df["label"]
    preds = model.predict(X)
    acc = accuracy_score(y, preds)
    report = {"accuracy": acc, "n_test": len(df)}
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(report, f)
    print(f"Wrote evaluation report to {report_path}")

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--test", required=True)
    p.add_argument("--report", required=True)
    args = p.parse_args()
    main(args.model, args.test, args.report)

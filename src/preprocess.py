import os
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split

def main(input_path, processed_output, test_output):
    # expect input_path to be a folder containing raw.csv
    raw_file = os.path.join(input_path, "raw.csv")
    df = pd.read_csv(raw_file)
    train, test = train_test_split(df, test_size=0.2, random_state=42)
    os.makedirs(processed_output, exist_ok=True)
    os.makedirs(test_output, exist_ok=True)
    train_path = os.path.join(processed_output, "train.csv")
    test_path = os.path.join(test_output, "test.csv")
    train.to_csv(train_path, index=False)
    test.to_csv(test_path, index=False)
    print(f"Wrote train to {train_path} and test to {test_path}")

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--processed_output", required=True)
    p.add_argument("--test_output", required=True)
    args = p.parse_args()
    main(args.input, args.processed_output, args.test_output)

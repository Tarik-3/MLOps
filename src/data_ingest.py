import os
import argparse
import pandas as pd

def main(output):
    os.makedirs(output, exist_ok=True)
    # simple synthetic dataset
    df = pd.DataFrame({
        "feature1": range(100),
        "feature2": [x * 0.5 for x in range(100)],
        "label": [0 if x < 50 else 1 for x in range(100)]
    })
    out_path = os.path.join(output, "raw.csv")
    df.to_csv(out_path, index=False)
    print(f"Wrote raw data to {out_path}")

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("--output", required=True)
    args = p.parse_args()
    main(args.output)

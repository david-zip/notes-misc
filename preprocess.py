"""Feature engineers the house price dataset."""
import boto3
import numpy as np
import pandas as pd
import pathlib
import argparse

if __name__ == "__main__":
    print("Starting preprocessing.")
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-data", type=str, required=True)
    args = parser.parse_args()

    print("Downloading data")
    base_dir = "/opt/ml/processing"
    pathlib.Path(f"{base_dir}/data").mkdir(parents=True, exist_ok=True)
    input_data = args.input_data
    bucket = input_data.split("/")[2]
    key = "/".join(input_data.split("/")[3:])

    print("Reading data")
    fn = f"{base_dir}/data/Housing.csv"
    s3 = boto3.resource("s3")
    s3.Bucket(bucket).download_file(key, fn)
    raw_data = pd.read_csv(fn)

    print("Defining transformers.")
    boolmap = {
        "yes": 1,
        "no": 0
    }

    catemap = {
        "furnished": 2, 
        "semi-furnished": 1, 
        "unfurnished": 0
    }

    processed_data = raw_data.replace({
                                    "mainroad": boolmap,
                                    "guestroom": boolmap,
                                    "basement": boolmap,
                                    "hotwaterheating": boolmap,
                                    "airconditioning": boolmap,
                                    "prefarea": boolmap,
                                    "furnishingstatus": catemap
                      })

    print("Applying transforms.")
    print("Splitting %d rows of data into train, validation, test datasets.", len(processed_data))
    train, test, validation = np.split(processed_data, [int(0.7 * len(processed_data)), int(0.85 * len(processed_data))])

    print("Writing out datasets to %s.", base_dir)
    pd.DataFrame(train).to_csv(f"{base_dir}/train/train.csv", header=False, index=False)
    pd.DataFrame(validation).to_csv(f"{base_dir}/validation/validation.csv", header=False, index=False)
    pd.DataFrame(test).to_csv(f"{base_dir}/test/test.csv", header=False, index=False)

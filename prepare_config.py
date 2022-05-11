import argparse
import json


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--config_file", help="Path to chalice config json file", required=True)
    parser.add_argument("--output_file", help="Path to chalice config output", required=True)
    parser.add_argument("--iam_role_arn", help="IAM role arn for lambda", required=True)
    parser.add_argument("--subnet_ids", help="Comma-separated list of subnet ids", required=True)
    known_args, *_ = parser.parse_known_args()

    with open(known_args.config_file, "r") as json_file:
        config = json.load(json_file)

    config["stages"]["dev"]["iam_role_arn"] = known_args.iam_role_arn
    config["stages"]["dev"]["subnet_ids"] = known_args.subnet_ids.split(",")

    with open(known_args.output_file, "w") as json_file:
        json.dump(config, json_file)

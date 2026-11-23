"""Reload and score the frozen held-out ticket fixture."""

import argparse
import csv
import json
import math
from pathlib import Path

from train import tokens


def predict(artifact, text):
    vocabulary = set(artifact["vocabulary"])
    words = [word for word in tokens(text) if word in vocabulary]
    total_documents = sum(artifact["document_counts"].values())
    vocabulary_size = len(vocabulary)
    scores = {}
    for label in artifact["labels"]:
        counts = artifact["token_counts"][label]
        token_total = sum(counts.values())
        score = math.log(artifact["document_counts"][label] / total_documents)
        score += sum(
            math.log((counts.get(word, 0) + artifact["alpha"]) / (token_total + artifact["alpha"] * vocabulary_size))
            for word in words
        )
        scores[label] = score
    return max(artifact["labels"], key=lambda label: (scores[label], label))


def evaluate(rows, predictions, labels):
    confusion = {label: {other: 0 for other in labels} for label in labels}
    for row, predicted in zip(rows, predictions):
        confusion[row["label"]][predicted] += 1
    report = {}
    for label in labels:
        tp = confusion[label][label]
        fp = sum(confusion[actual][label] for actual in labels if actual != label)
        fn = sum(confusion[label][other] for other in labels if other != label)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        report[label] = {"support": tp + fn, "precision": precision, "recall": recall, "f1": f1}
    return confusion, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--data", type=Path, default=Path(__file__).with_name("test.csv"))
    args = parser.parse_args()
    artifact = json.loads(args.model.read_text(encoding="utf-8"))
    if artifact.get("format") != "multinomial-naive-bayes-v1":
        raise ValueError("unsupported model artifact format")
    with args.data.open(encoding="utf-8", newline="") as source:
        rows = list(csv.DictReader(source))
    predictions = [predict(artifact, row["text"]) for row in rows]
    confusion, report = evaluate(rows, predictions, artifact["labels"])
    print("ticket_id,actual,predicted")
    for row, predicted in zip(rows, predictions):
        print(f"{row['ticket_id']},{row['label']},{predicted}")
    print("confusion_rows=actual,columns=predicted")
    for actual in artifact["labels"]:
        print(f"{actual}: " + ",".join(f"{predicted}={confusion[actual][predicted]}" for predicted in artifact["labels"]))
    print("class_metrics=class,support,precision,recall,f1")
    for label in artifact["labels"]:
        result = report[label]
        print(f"{label},{result['support']},{result['precision']:.3f},{result['recall']:.3f},{result['f1']:.3f}")


if __name__ == "__main__":
    main()

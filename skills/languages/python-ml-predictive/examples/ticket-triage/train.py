"""Train a small multinomial Naive Bayes text classifier using only stdlib."""

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokens(text):
    words = TOKEN_RE.findall(text.lower())
    return words + [f"{left} {right}" for left, right in zip(words, words[1:])]


def read_rows(path):
    with Path(path).open(encoding="utf-8", newline="") as source:
        rows = list(csv.DictReader(source))
    if not rows or any(not row["ticket_id"] or not row["text"] or not row["label"] for row in rows):
        raise ValueError("training CSV must contain ticket_id, text, and label values")
    return rows


def train(rows):
    labels = sorted({row["label"] for row in rows})
    if len(labels) < 2:
        raise ValueError("training requires at least two classes")
    label_counts = Counter(row["label"] for row in rows)
    token_counts = defaultdict(Counter)
    vocabulary = set()
    for row in rows:
        row_tokens = tokens(row["text"])
        token_counts[row["label"]].update(row_tokens)
        vocabulary.update(row_tokens)
    return {
        "format": "multinomial-naive-bayes-v1",
        "labels": labels,
        "document_counts": dict(label_counts),
        "token_counts": {label: dict(token_counts[label]) for label in labels},
        "vocabulary": sorted(vocabulary),
        "alpha": 1.0,
        "tokenizer": "lowercase alphanumeric unigrams and adjacent bigrams",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path(__file__).with_name("train.csv"))
    parser.add_argument("--model", type=Path, required=True)
    args = parser.parse_args()
    artifact = train(read_rows(args.data))
    args.model.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    print(f"trained_rows={sum(artifact['document_counts'].values())}")
    print(f"classes={','.join(artifact['labels'])}")
    print(f"vocabulary_size={len(artifact['vocabulary'])}")
    print(f"model={args.model}")


if __name__ == "__main__":
    main()

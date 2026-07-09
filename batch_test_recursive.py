"""
batch_test_recursive.py

Like batch_test.py, but walks into subfolders recursively and prints
the raw model prediction for every image, plus a summary of how often
each class was predicted overall — useful for spotting whether the
model is defaulting to certain classes across your whole dataset.

Usage:
    python batch_test_recursive.py test_image
"""

import os
import sys
from collections import Counter
from PIL import Image

from predict import predict

SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".bmp")


def main():
    if len(sys.argv) != 2:
        print("Usage: python batch_test_recursive.py path/to/folder")
        sys.exit(1)

    root = sys.argv[1]
    if not os.path.isdir(root):
        print(f"Not a folder: {root}")
        sys.exit(1)

    prediction_counts = Counter()
    per_true_folder_predictions = {}
    total = 0
    failed = 0

    print(f"{'True folder':<15}{'File':<35}{'Predicted':<18}{'Confidence'}")
    print("-" * 85)

    for dirpath, _, filenames in os.walk(root):
        image_files = sorted(
            f for f in filenames if f.lower().endswith(SUPPORTED_EXTENSIONS)
        )
        if not image_files:
            continue

        true_folder = os.path.relpath(dirpath, root)
        if true_folder == ".":
            true_folder = "(root)"

        per_true_folder_predictions.setdefault(true_folder, Counter())

        for filename in image_files:
            filepath = os.path.join(dirpath, filename)
            try:
                image = Image.open(filepath).convert("RGB")
                pred, confidence, _ = predict(image)
            except Exception as e:
                print(f"{true_folder:<15}{filename:<35}FAILED — {e}")
                failed += 1
                continue

            total += 1
            prediction_counts[pred] += 1
            per_true_folder_predictions[true_folder][pred] += 1

            print(f"{true_folder:<15}{filename:<35}{pred:<18}{confidence:.1f}%")

    print("-" * 85)
    print(f"\nTotal images processed: {total}  (failed: {failed})\n")

    print("Overall prediction distribution (what the model guessed, across everything):")
    for label, count in prediction_counts.most_common():
        pct = 100 * count / total if total else 0
        print(f"  {label:<15} {count:<6} ({pct:.1f}%)")

    print("\nPer-true-folder prediction breakdown:")
    for true_folder, counts in per_true_folder_predictions.items():
        folder_total = sum(counts.values())
        print(f"\n  {true_folder} ({folder_total} images):")
        for label, count in counts.most_common():
            pct = 100 * count / folder_total if folder_total else 0
            print(f"    -> predicted {label:<15} {count:<6} ({pct:.1f}%)")


if __name__ == "__main__":
    main()
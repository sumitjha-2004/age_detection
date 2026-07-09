"""
test_folders.py

Runs the model against images organized in ground-truth folders
(18-20/, 21-30/, 31-40/, 41-50/, 51-60/) and reports accuracy,
mapping the model's 9 native classes down to these 5 folders.

Usage:
    python test_folders.py test_image
"""

import os
import sys
from collections import defaultdict
from PIL import Image

from predict import predict

SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".bmp")

# Maps the model's native 9-class output down to your 5 folder buckets.
# Approximate: the model's "10-19" bucket spans ages 10-19, while your
# "18-20" folder is really just 18-20 — there's no exact overlap, this
# is the closest reasonable mapping, not a perfect one.
PREDICTION_TO_FOLDER = {
    "10-19": "18-20",
    "20-29": "21-30",
    "30-39": "31-40",
    "40-49": "41-50",
    "50-59": "51-60",
}


def main():
    if len(sys.argv) != 2:
        print("Usage: python test_folders.py path/to/test_image")
        sys.exit(1)

    root = sys.argv[1]
    if not os.path.isdir(root):
        print(f"Not a folder: {root}")
        sys.exit(1)

    folder_names = sorted(
        f for f in os.listdir(root)
        if os.path.isdir(os.path.join(root, f))
    )

    if not folder_names:
        print(f"No subfolders found in {root}")
        sys.exit(1)

    total_correct = 0
    total_count = 0
    per_folder_correct = defaultdict(int)
    per_folder_total = defaultdict(int)

    print(f"{'File':<35}{'True':<10}{'Predicted (raw)':<18}{'Mapped':<10}{'Conf':<10}{'Result'}")
    print("-" * 95)

    for true_label in folder_names:
        folder_path = os.path.join(root, true_label)
        image_files = sorted(
            f for f in os.listdir(folder_path)
            if f.lower().endswith(SUPPORTED_EXTENSIONS)
        )

        for filename in image_files:
            filepath = os.path.join(folder_path, filename)
            try:
                image = Image.open(filepath).convert("RGB")
                raw_pred, confidence, _ = predict(image)
            except Exception as e:
                print(f"{filename:<35}FAILED — {e}")
                continue

            mapped_pred = PREDICTION_TO_FOLDER.get(raw_pred, "out-of-range")
            is_correct = (mapped_pred == true_label)

            total_count += 1
            per_folder_total[true_label] += 1
            if is_correct:
                total_correct += 1
                per_folder_correct[true_label] += 1

            result = "MATCH" if is_correct else "miss"
            print(f"{filename:<35}{true_label:<10}{raw_pred:<18}{mapped_pred:<10}{confidence:.1f}%     {result}")

    print("-" * 95)
    print(f"\nOverall: {total_correct}/{total_count} correct "
          f"({100 * total_correct / total_count:.1f}%)\n" if total_count else "No images found.\n")

    print("Per-folder breakdown:")
    for folder in folder_names:
        t = per_folder_total[folder]
        c = per_folder_correct[folder]
        if t == 0:
            print(f"  {folder:<10} no images found")
            continue
        print(f"  {folder:<10} {c}/{t} correct ({100*c/t:.1f}%)")


if __name__ == "__main__":
    main()
"""
Train a pothole detector and export it as pothole.onnx for pothole-detector.html

Setup (a free Google Colab GPU is enough; a laptop CPU is too slow):
    pip install ultralytics

Dataset:
    Download a pothole dataset in "YOLOv8" format. Good starting points:
      - Roboflow Universe: search "pothole" and download in YOLOv8 format
      - RDD2022 road-damage dataset (has an India subset): convert only the pothole
        class (D40) to a single class called "pothole"
    Prefer data from Indian roads: shadows, patched tar, speed breakers and waterlogged
    patches are the usual false positives, so include such images as negatives.
    The dataset folder must contain a data.yaml with train/val paths and: names: [pothole]

Run:
    python train_pothole_yolo.py --data path/to/data.yaml --epochs 60

Output:
    pothole.onnx next to this script. Load it in the page with "Load model (.onnx)",
    or keep it in the same folder as the page and serve both with:  python -m http.server
"""
import argparse
import shutil
from pathlib import Path

from ultralytics import YOLO


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="path to data.yaml")
    ap.add_argument("--epochs", type=int, default=60)
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--base", default="yolov8n.pt",
                    help="yolov8n.pt = fastest (best for in-browser use); yolov8s.pt = more accurate but slower")
    args = ap.parse_args()

    model = YOLO(args.base)
    model.train(data=args.data, epochs=args.epochs, imgsz=640, batch=args.batch, patience=15)

    best = Path(model.trainer.best)
    print("Best weights:", best)
    metrics = YOLO(str(best)).val(data=args.data, imgsz=640)
    print(f"mAP50 = {metrics.box.map50:.3f}  (check this on images from YOUR roads before trusting it)")

    # The page expects a fixed 640x640 input and a single [1, 5, 8400] output.
    onnx_path = YOLO(str(best)).export(format="onnx", imgsz=640, opset=12, simplify=True, dynamic=False)
    shutil.copy(onnx_path, "pothole.onnx")
    print("Saved pothole.onnx")


if __name__ == "__main__":
    main()

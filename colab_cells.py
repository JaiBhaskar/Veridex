# Run each block as a separate Colab cell (Runtime > Change runtime type > T4 GPU first).

# --- Cell 1: install
# !pip install -q ultralytics

# --- Cell 2: download the dataset from Roboflow
# Paste the "Jupyter" download code from your forked dataset (YOLOv8 format). It ends with a variable called `dataset`.

# --- Cell 3: fix the data.yaml paths
import os, yaml
root = dataset.location
def pick(*names):
    for n in names:
        p = os.path.join(root, n, "images")
        if os.path.isdir(p): return p
cfg = yaml.safe_load(open(f"{root}/data.yaml"))
cfg["train"] = pick("train")
cfg["val"] = pick("valid", "val", "test") or cfg["train"]
cfg.pop("test", None); cfg.pop("path", None)
yaml.safe_dump(cfg, open(f"{root}/data.yaml", "w"))
print(cfg)

# --- Cell 4: train, export to ONNX, download
import shutil
from ultralytics import YOLO
from google.colab import files

m = YOLO("yolov8n.pt")
m.train(data=f"{root}/data.yaml", epochs=60, imgsz=640, batch=16, patience=15)
out = YOLO(str(m.trainer.best)).export(format="onnx", imgsz=640, opset=12, simplify=True, dynamic=False)
shutil.copy(out, "/content/pothole.onnx")
files.download("/content/pothole.onnx")

# --- Cell 5 (optional): check the exported model
# import onnx, os
# m = onnx.load("/content/pothole.onnx")
# print("OK", round(os.path.getsize("/content/pothole.onnx")/1e6, 1), "MB")
# print([(o.name, [d.dim_value for d in o.type.tensor_type.shape.dim]) for o in m.graph.output])   # expect [1, 5, 8400]

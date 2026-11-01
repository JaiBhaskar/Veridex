VERIDEX pothole project: website and detection code

pothole-detector.html   The website detector page (HTML + CSS + JavaScript, one file).
                        It downloads pothole.onnx from the same folder, runs the detection model in the
                        browser (ONNX Runtime Web), finds the road from GPS, checks warranty and writes the complaint.
train_pothole_yolo.py   Python script that trains the YOLOv8 pothole model and exports pothole.onnx.
colab_cells.py          The Google Colab cells used to download the dataset, train and export the model.

Languages: JavaScript/HTML/CSS (website and detection in the browser), Python (model training).

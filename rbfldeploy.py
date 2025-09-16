from roboflow.core.version import Version
from roboflow import Roboflow

rf = Roboflow(api_key="B1IovfYIG6d7q9rSBBG1")
project = rf.workspace().project(r"auto-time-classify")
version = project.version(4)
version.deploy("yolov8-cls","runs/classify/classifyv4-no-multiclass/weights/","best.pt")
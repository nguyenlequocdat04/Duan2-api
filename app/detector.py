from imageai.Detection.Custom import CustomObjectDetection
from app.config import DefaultConfig
import os

img_path = DefaultConfig.UPLOAD_FOLDER
result_dir = DefaultConfig.RESULT_FOLDER

model_isloaded = False # not loaded
detector = None
# ==========
def load_model():
    global detector, model_isloaded
    if not model_isloaded:
        detector = CustomObjectDetection()
        detector.setModelTypeAsYOLOv3()
        detector.setModelPath(f"{DefaultConfig.MODEL_PATH}/banhmi-detector.h5")
        detector.setJsonPath(f"{DefaultConfig.MODEL_PATH}/detection_config-banhmi.json")
        detector.loadModel()
        model_isloaded = 1
        print("Loaded model!!")
    return detector
# ===========
def DetectImg(img_name):
    global detector
    if(img_name is not None):
        if not model_isloaded:
            load_model()

        detections = detector.detectObjectsFromImage(input_image=f"{img_path}/{img_name}", output_image_path=f"{result_dir}/{img_name}")
        
        for detection in detections:
            print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])
    else:
        if(not model_isloaded):
            LoadModel() 
        return None 

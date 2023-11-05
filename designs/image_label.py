import tensorflow as tf
import numpy as np

from django.http import JsonResponse
from PIL import Image

def load_labels(filename):
  with open(filename, 'r') as f:
    return [line.strip() for line in f.readlines()]

def classify_image(request):
    """Takes an uploaded image as a query and returns the predictions."""
    image_file = request.FILES["image"]
    
    #Load model
    interpreter = tf.lite.Interpreter(model_path="designs\models\DoD-Model.tflite")
    interpreter.allocate_tensors()
    
     # Get the input and output details of the model.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # check the type of the input tensor
    floating_model = input_details[0]['dtype'] == np.float32
   
    #Prepare the input data
    img = Image.open(image_file)
    img=img.resize((input_details[0]['shape'][1], input_details[0]['shape'][2]))
    input_data = (img - 127.5) / 127.5
    
    #Set the inpout tensor of the model
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    
    #Get output data of the model
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    #Squeeze to remove extra dimensions
    results = np.squeeze(output_data)
    
    top_n = results.argsort()[-5:][::-1]
    
    labels = load_labels("designs\models\labels.txt")
    
    top_predictions = labels[top_n[0]]
    top_score = float(results[top_n[0]])
    
    predictions = []
    for i in top_n:
        prediction={
            "label": labels[i],
            "confidence": float(results[i])
        }
        predictions.append(prediction)
        
    return {
        "top_predictions": top_predictions,
        "top_score": top_score,
        "predictions": predictions,
    }
    
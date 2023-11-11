import tensorflow as tf
import numpy as np

from django.http import JsonResponse
from PIL import Image
from tensorflow import keras

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
    
    floating_model = input_details[0]['dtype'] == np.float32
   
    #Prepare the input data
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]
    img = Image.open(image_file).resize((width, height))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    # score = tf.nn.softmax(predictions[0])
    
    # img = np.frombuffer(img.tobytes(), dtype=np.uint8)
    
    # input_data = np.expand_dims(img, axis=0)
    
    if floating_model:
        input_data = (np.float32(img) - 127.5) / 127.5
        
    #Set the inpout tensor of the model
    interpreter.set_tensor(input_details[0]['index'], img_array)
    interpreter.invoke()
    
    #Get output data of the model
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    #Squeeze to remove extra dimensions
    results = np.squeeze(output_data)
    
    softmax_output = tf.nn.softmax(results)
    
    score = softmax_output.numpy()
    
    top_n = np.argsort(score)[-5:][::-1]
    
    labels = load_labels("designs\models\labels.txt")
    
    top_predictions = labels[top_n[0]].replace("_", " ").title()
    top_score = "{:.2f}%".format(score[top_n[0]] * 100)
    
    predictions = []
    for i in top_n[1:]:
        prediction={
            "label": labels[i].replace("_", " ").title(),
            "confidence": "{:.2f}%" .format(score[i]*100),
        }
        predictions.append(prediction)

    final_result = {
    "top_predictions": top_predictions,
    "top_score": top_score,
    "other_predictions": predictions,
    }
    return final_result
    
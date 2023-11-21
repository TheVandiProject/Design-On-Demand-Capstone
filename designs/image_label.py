import tensorflow as tf
import numpy as np

from django.http import JsonResponse
from PIL import Image
from tensorflow import keras

def load_labels(filename):
  with open(filename, 'r') as f:
    return [line.strip() for line in f.readlines()]

def classify_image(request):
    """Takes an uploaded image as a query and returns the predictions for two models."""
    image_file = request.FILES["image"]
    
    # Load the first model
    interpreter1 = tf.lite.Interpreter(model_path="designs\models\DoD-Model.tflite")
    interpreter1.allocate_tensors()
    
    # Get the input and output details of the first model
    input_details1 = interpreter1.get_input_details()
    output_details1 = interpreter1.get_output_details()
    
    # Load the second model
    interpreter2 = tf.lite.Interpreter(model_path="designs\models\Second-DoD-Model.tflite")
    interpreter2.allocate_tensors()
    
    # Get the input and output details of the second model
    input_details2 = interpreter2.get_input_details()
    output_details2 = interpreter2.get_output_details()
    
    # Prepare the input data for the first model
    height1, width1 = input_details1[0]['shape'][1], input_details1[0]['shape'][2]
    img1 = Image.open(image_file).resize((width1, height1))
    img_array1 = tf.keras.utils.img_to_array(img1)
    img_array1 = tf.expand_dims(img_array1, 0)  # Create a batch for the first model
    
    # Set the input tensor of the first model
    interpreter1.set_tensor(input_details1[0]['index'], img_array1)
    interpreter1.invoke()
    
    # Get the output data of the first model
    output_data1 = interpreter1.get_tensor(output_details1[0]['index'])
    results1 = np.squeeze(output_data1)
    
    # Process results for the first model
    softmax_output1 = tf.nn.softmax(results1)
    score1 = softmax_output1.numpy()
    top_n1 = np.argsort(score1)[-5:][::-1]
    
    labels1 = load_labels("designs\models\labels.txt")
    
    predictions1 = []
    for i in top_n1:
        prediction1 = {
            "label": labels1[i].replace("_", " ").title(),
            "confidence": "{:.2f}%".format(score1[i] * 100),
        }
        predictions1.append(prediction1)
    
    # Prepare the input data for the second model
    height2, width2 = input_details2[0]['shape'][1], input_details2[0]['shape'][2]
    img_array2 = tf.image.resize(img_array1, [height2, width2])  # Resize for the second model
    
    # Set the input tensor of the second model
    interpreter2.set_tensor(input_details2[0]['index'], img_array2)
    interpreter2.invoke()
    
    # Get the output data of the second model
    output_data2 = interpreter2.get_tensor(output_details2[0]['index'])
    results2 = np.squeeze(output_data2)
    
    # Process results for the second model
    softmax_output2 = tf.nn.softmax(results2)
    score2 = softmax_output2.numpy()
    top_n2 = np.argsort(score2)[-5:][::-1]
    
    labels2 = load_labels("designs\models\labels.txt")  # Replace with the correct labels file
    
    predictions2 = []
    for i in top_n2:
        prediction2 = {
            "label": labels2[i].replace("_", " ").title(),
            "confidence": "{:.2f}%".format(score2[i] * 100),
        }
        predictions2.append(prediction2)
    
    # Merge results and keep the highest confidence for shared labels
    merged_predictions = {}
    for prediction in predictions1 + predictions2:
        label = prediction["label"]
        confidence = float(prediction["confidence"][:-1])  # Remove '%' and convert to float
        
        if label in merged_predictions:
            # Update with the highest confidence
            merged_predictions[label] = max(merged_predictions[label], confidence)
        else:
            merged_predictions[label] = confidence
    
    # Sort by confidence in descending order
    sorted_merged_predictions = [
        {"label": label, "confidence": f"{confidence:.2f}%", "score": confidence} 
        for label, confidence in sorted(merged_predictions.items(), key=lambda x: x[1], reverse=True)
    ]
    
    # Separate the top prediction and other predictions
    top_prediction = sorted_merged_predictions[0]
    other_predictions = sorted_merged_predictions[1:5]
    
    # Take the top 5 results
    final_result = {
        "top_predictions": top_prediction["label"],
        "top_score": top_prediction["confidence"],
        "other_predictions": other_predictions,
    }
    
    return final_result

    
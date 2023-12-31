import os
import io
import random

import numpy as np
import tensorflow as tf
import boto3
import requests
from PIL import Image
from storages.backends.s3boto3 import S3Boto3Storage
from DesignOnDemand.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME


class S3GetMediaUploadsStorage(S3Boto3Storage):
    location = 'media/uploads/'

def get_uploaded_images(request):
    try:
        base_url = f'https://s3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/'
        
        # List files in the S3 bucket
        objects = S3DesignerDesignsStorage().bucket.objects.filter(Prefix=f"media/uploads/")

        # Extract image URLs directly from S3 storage
        images = [{'image_url': f'{base_url}{obj.key}'} for obj in objects if obj.size > 0]

        return images
    except Exception as e:
        return []

class S3DesignerDesignsStorage(S3Boto3Storage):
    location = 'media/designer-uploads/'
    

def get_designer_images(request):
    try:
        base_url = f'https://s3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/'
        
        # List files in the S3 bucket
        objects = S3DesignerDesignsStorage().bucket.objects.filter(Prefix=f"media/designer-uploads/")

        # Extract image URLs directly from S3 storage
        images = [{'image_url': f'{base_url}{obj.key}'} for obj in objects if obj.size > 0]

        return images
    except Exception as e:
        return []
    

def load_labels(filename):
  with open(filename, 'r') as f:
    return [line.strip() for line in f.readlines()]

class S3ImageStorage(S3Boto3Storage):
    location = 'static/designs/images/'  # adjust this based on your S3 bucket structure

def get_random_images(label, num_images=10):
    try:
        base_url = f'https://s3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/'  # Adjust this based on your S3 bucket structure
        images = []

        # List files in the S3 bucket
        objects = S3ImageStorage().bucket.objects.filter(Prefix=f"static/designs/images/{label}/")

        for obj in objects:
            if obj.size > 0:
                image_url = f'{base_url}{obj.key}'
                images.append(image_url)

        if not images:
            return []

        return random.sample(images, min(num_images, len(images)))
    except Exception as e:
        return []
    
class S3MLStorage(S3Boto3Storage):
    location = 'static/designs/models/'


def classify_image(image_url):
    """Takes an uploaded image as a query and returns the predictions."""
    
    aws_access_key_id = AWS_ACCESS_KEY_ID
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    bucket_name = AWS_STORAGE_BUCKET_NAME
    
    # Download model file
    model_file_name = 'static/models/Diverse_Model-DoD.tflite'
    local_model_file_name = os.path.join(os.getcwd(), model_file_name.replace('/', os.sep))
    os.makedirs(os.path.dirname(local_model_file_name), exist_ok=True)
    s3.download_file(bucket_name, model_file_name, local_model_file_name)

    # Download label file
    label_file_name = 'static/models/labels/detailed-labels.txt'
    local_label_file_name = os.path.join(os.getcwd(), label_file_name.replace('/', os.sep))
    os.makedirs(os.path.dirname(local_label_file_name), exist_ok=True)
    s3.download_file(bucket_name, label_file_name, local_label_file_name)

    #Load labels
    labels = load_labels(local_label_file_name)
    
    #Load model
    # interpreter = tf.lite.Interpreter(model_path="designs\models\Diverse_Model-DoD.tflite")
    interpreter = tf.lite.Interpreter(model_path=model_file_name)

    interpreter.allocate_tensors()
    
     # Get the input and output details of the model.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    #Get the Image from S3
    response = requests.get(image_url)
    response.raise_for_status()
   
    #Prepare the input data
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]
    img = Image.open(io.BytesIO(response.content)).resize((width, height))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch
        
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
    
    top_predictions = labels[top_n[0]].replace("_", " ").title()
    top_score = "{:.2f}%".format(score[top_n[0]] * 100)
    top_images = get_random_images(top_predictions)
    
    predictions = []
    for i in top_n[1:]:
        if 0 <= i < len(labels):
            label_title = labels[i].replace("_", " ").title()
            confidence = "{:.2f}%" .format(score[i]*100)
            images = get_random_images(label_title)
            
            
            prediction={
                "label": label_title,
                "confidence": confidence,
                "images": images,
            }
            predictions.append(prediction)     
        else:
            prediction={
                # "label": f"Invalid index: {i}",
                "label": "Other",
                "confidence": "{:.2f}%" .format(score[i]*100),
                images: [],
            }
            predictions.append(prediction)

    final_result = {
    "top_predictions": top_predictions,
    "top_score": top_score, #Used mostly for development reasons
    "top_images": top_images,
    "other_predictions": predictions,
    }
    return final_result
    # """Takes an uploaded image as a query and returns the predictions for two models."""
    # image_file = request.FILES["image"]
    
    # # Load the first model
    # interpreter1 = tf.lite.Interpreter(model_path="designs\models\DoD-Model.tflite")
    # interpreter1.allocate_tensors()
    
    # # Get the input and output details of the first model
    # input_details1 = interpreter1.get_input_details()
    # output_details1 = interpreter1.get_output_details()
    
    # # Load the second model
    # interpreter2 = tf.lite.Interpreter(model_path="designs\models\Second-DoD-Model.tflite")
    # interpreter2.allocate_tensors()
    
    # # Get the input and output details of the second model
    # input_details2 = interpreter2.get_input_details()
    # output_details2 = interpreter2.get_output_details()
    
    # # Prepare the input data for the first model
    # height1, width1 = input_details1[0]['shape'][1], input_details1[0]['shape'][2]
    # img1 = Image.open(image_file).resize((width1, height1))
    # img_array1 = tf.keras.utils.img_to_array(img1)
    # img_array1 = tf.expand_dims(img_array1, 0)  # Create a batch for the first model
    
    # # Set the input tensor of the first model
    # interpreter1.set_tensor(input_details1[0]['index'], img_array1)
    # interpreter1.invoke()
    
    # # Get the output data of the first model
    # output_data1 = interpreter1.get_tensor(output_details1[0]['index'])
    # results1 = np.squeeze(output_data1)
    
    # # Process results for the first model
    # softmax_output1 = tf.nn.softmax(results1)
    # score1 = softmax_output1.numpy()
    # top_n1 = np.argsort(score1)[-5:][::-1]
    
    # labels1 = load_labels("designs\models\labels.txt")
    
    # predictions1 = []
    # for i in top_n1:
    #     prediction1 = {
    #         "label": labels1[i].replace("_", " ").title(),
    #         "confidence": "{:.2f}%".format(score1[i] * 100),
    #     }
    #     predictions1.append(prediction1)
    
    # # Prepare the input data for the second model
    # height2, width2 = input_details2[0]['shape'][1], input_details2[0]['shape'][2]
    # img_array2 = tf.image.resize(img_array1, [height2, width2])  # Resize for the second model
    
    # # Set the input tensor of the second model
    # interpreter2.set_tensor(input_details2[0]['index'], img_array2)
    # interpreter2.invoke()
    
    # # Get the output data of the second model
    # output_data2 = interpreter2.get_tensor(output_details2[0]['index'])
    # results2 = np.squeeze(output_data2)
    
    # # Process results for the second model
    # softmax_output2 = tf.nn.softmax(results2)
    # score2 = softmax_output2.numpy()
    # top_n2 = np.argsort(score2)[-5:][::-1]
    
    # labels2 = load_labels("designs\models\labels.txt")  # Replace with the correct labels file
    
    # predictions2 = []
    # for i in top_n2:
    #     prediction2 = {
    #         "label": labels2[i].replace("_", " ").title(),
    #         "confidence": "{:.2f}%".format(score2[i] * 100),
    #     }
    #     predictions2.append(prediction2)
    
    # # Merge results and keep the highest confidence for shared labels
    # merged_predictions = {}
    # for prediction in predictions1 + predictions2:
    #     label = prediction["label"]
    #     confidence = float(prediction["confidence"][:-1])  # Remove '%' and convert to float
        
    #     if label in merged_predictions:
    #         # Update with the highest confidence
    #         merged_predictions[label] = max(merged_predictions[label], confidence)
    #     else:
    #         merged_predictions[label] = confidence
    
    # # Sort by confidence in descending order
    # sorted_merged_predictions = [
    #     {"label": label, "confidence": f"{confidence:.2f}%", "score": confidence} 
    #     for label, confidence in sorted(merged_predictions.items(), key=lambda x: x[1], reverse=True)
    # ]
    
    # # Separate the top prediction and other predictions
    # top_prediction = sorted_merged_predictions[0]
    # other_predictions = sorted_merged_predictions[1:5]
    
    # # Take the top 5 results
    # final_result = {
    #     "top_predictions": top_prediction["label"],
    #     "top_score": top_prediction["confidence"],
    #     "other_predictions": other_predictions,
    # }
    
    # return final_result

    
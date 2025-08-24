import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event.get("bucket")
    key = event.get("s3_key")

    if not bucket or not key:
        return {
            "statusCode": 400,
            "body": "Error: 'bucket' or 's3_key' missing in event"
        }## TODO: fill in
    
    # Download the data from s3 to /tmp/image.png
    ## TODO: fill in
    s3.download_file(bucket,key,"/tmp/image.png")
    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }


import json
# import sagemaker
import base64
import boto3
# from sagemaker.serializers import IdentitySerializer
runtime = boto3.client('sagemaker-runtime')
# Fill this in with the name of your deployed model
ENDPOINT = "image-classification-2025-08-21-15-19-40-164" ## TODO: fill in

def lambda_handler(event, context):
    image_data = event.get("image_data")
    
    if not image_data:
        return {
            "statusCode": 400,
            "body": "Missing 'image_data' in request."
        }
    
    image = base64.b64decode(image_data)
    
    # continue processing...
    return {
        "statusCode": 200,
        "body": "Image processed successfully!"
    }

    # Instantiate a Predictor
    predictor = runtime.invoke_endpoint(
        EndpointName = ENDPOINT,
        ContentType='image/png',
        Body=image
    )

    # # For this model the IdentitySerializer needs to be "image/png"
    # predictor.serializer = IdentitySerializer("image/png")
    
    # Make a prediction:
    inferences = predictor['Body'].read().decode('utf-8')## TODO: fill in
    
    # We return the data back to the Step Function    
    event["inferences"] = inferences
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }

import json


THRESHOLD = .93


def lambda_handler(event, context):
    # Safely get "inferences" key
    inferences = event.get("inferences")

    if inferences is None:
        return {
            "statusCode": 400,
            "body": "Error: 'inferences' key not found in event"
        }

    # Process inferences
    return {
        "statusCode": 200,
        "body": inferences
    }
    
    # Check if any values in our inferences are above THRESHOLD
    meets_threshold = max(inferences) > THRESHOLD ## TODO: fill in
    
    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if meets_threshold:
        pass
    else:
        raise("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }

import json
from PIL import Image
from io import BytesIO
from azure.storage.blob import BlobServiceClient
from http import HTTPStatus
import numpy as np
import time
import json
import cv2


def handle(event, context):
    try:
        print("testing")
        connection_string = "DefaultEndpointsProtocol=https;AccountName=imageworkflow;AccountKey=RvWg7QSEhof25ngK9R9DxUKgfhgcSAEM8jq5p66NQF3gt2uel/9xKffRXC79PAyIkthnMBjZkXcp+AStAV6Kpw==;EndpointSuffix=core.windows.net"
        source_container_name = "incoming-images-of"  # Container with the original image
        target_container_name = "masked-images-of"  # Container where the resized image will be stored
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        container_client = blob_service_client.get_container_client(source_container_name)
        max_retries = 100
        wait_time = 0.1  # seconds to wait between retries

        found = False  # Flag to indicate whether a blob has been found

        for attempt in range(max_retries):
            blob_list = list(container_client.list_blobs())

            if blob_list:
                found = True
                print("**** Found *****")
                break  # Exit the loop if a blob is found

            print(f"No blobs found, retrying in {wait_time} seconds... (Attempt {attempt + 1} of {max_retries})")
            time.sleep(wait_time)

        if not found:
            # If no blobs are found after all attempts, return an error response
            return {
                "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
                "body": json.dumps({"error": str(e)})
            }
        
        blob_name = blob_list[0].name  # Since there's only one blob, get its name
        blob_client = blob_service_client.get_blob_client(container=source_container_name, blob=blob_name)

        # Download the blob
        blob_data = blob_client.download_blob().readall()

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        # Load the image from the BytesIO stream
        face_image = Image.open(BytesIO(blob_data))
        
        # Convert the image to OpenCV format
        img = cv2.cvtColor(np.array(face_image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces with adjusted parameters
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

        # Load the Batman mask image
        mask_image = Image.open("function/batman-mask.png").convert("RGBA")

        # Filter out face candidates that are too small or not in the expected region
        for (x, y, w, h) in faces:
            print("** entered ****")
            # Define a threshold for the face size (for example, discard faces smaller than 100x100)
            if w > 100 and h > 100 and y < gray.shape[0] // 2:
                print("** face found ****")
                # Resize mask to fit the face
                mask_resized = mask_image.resize((int(w*1.5), int(h*1.5)))
                
                # Define the position to place the mask
                position = (x- int(0.19 * mask_resized.width), y - int(0.47 * mask_resized.height))
                
                # Convert OpenCV image to PIL format
                img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                
                # Paste the mask onto the original image
                img_pil.paste(mask_resized, position, mask_resized)
                
                # Convert back to OpenCV format
                img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    # Convert back to PIL image
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        
        
        # Save the processed image to a BytesIO stream
        output_stream = BytesIO()
        img_pil.save(output_stream, format=face_image.format or 'JPEG')
        output_stream.seek(0)  # Reset the stream position

        cv2.imwrite('face-image-with-mask.jpg', img)
        print("Processed image saved as face-image-with-mask.jpg")

        # Upload the resized image to the target container
        target_blob_client = blob_service_client.get_blob_client(container=target_container_name, blob=f"masked_{blob_name}")
        target_blob_client.upload_blob(output_stream, blob_type="BlockBlob", overwrite=True)

        return {
            "statusCode": HTTPStatus.OK,
            "body": "Image masked, and uploaded successfully to the target container."
        }
    
    except Exception as e:
        return {
            "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
            "body": json.dumps({"error": str(e)})
        }

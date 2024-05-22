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
        source_container_name = "incoming-images-of"  
        target_container_name = "masked-images-of"  
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        container_client = blob_service_client.get_container_client(source_container_name)
        max_retries = 100
        wait_time = 0.1  

        found = False  

        for attempt in range(max_retries):
            blob_list = list(container_client.list_blobs())

            if blob_list:
                found = True
                break  

            print(f"No blobs found, retrying in {wait_time} seconds... (Attempt {attempt + 1} of {max_retries})")
            time.sleep(wait_time)

        if not found:
            return {
                "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
                "body": json.dumps({"error": str(e)})
            }
        
        blob_name = blob_list[0].name 
        blob_client = blob_service_client.get_blob_client(container=source_container_name, blob=blob_name)

        blob_data = blob_client.download_blob().readall()

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        face_image = Image.open(BytesIO(blob_data))

        img = cv2.cvtColor(np.array(face_image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

        mask_image = Image.open("function/batman-mask.png").convert("RGBA")

        for (x, y, w, h) in faces:
            if w > 100 and h > 100 and y < gray.shape[0] // 2:
                mask_resized = mask_image.resize((int(w*1.5), int(h*1.5)))
                position = (x- int(0.19 * mask_resized.width), y - int(0.47 * mask_resized.height))
                img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

                img_pil.paste(mask_resized, position, mask_resized)
                img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        
        output_stream = BytesIO()
        img_pil.save(output_stream, format=face_image.format or 'JPEG')
        output_stream.seek(0) 

        cv2.imwrite('face-image-with-mask.jpg', img)
        print("Processed image saved as face-image-with-mask.jpg")

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

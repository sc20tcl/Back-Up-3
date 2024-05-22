import azure.functions as func
import logging
from PIL import Image, ImageDraw, ImageFont
from azure.storage.blob import BlobServiceClient, BlobClient
import io
from io import BytesIO
import numpy as np
import cv2

app = func.FunctionApp()

@app.route("resize", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def resize(req: func.HttpRequest) -> func.HttpResponse:
    try:
        connection_string = "DefaultEndpointsProtocol=https;AccountName=imageworkflow;AccountKey=RvWg7QSEhof25ngK9R9DxUKgfhgcSAEM8jq5p66NQF3gt2uel/9xKffRXC79PAyIkthnMBjZkXcp+AStAV6Kpw==;EndpointSuffix=core.windows.net"
        if not connection_string:
            raise ValueError("Storage connection string ('imageworkflow_STORAGE') not found.")

        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        image_name = "masked_Steven_Gerrard.jpg" 

        source_container_name = "masked-images"
        blob_client = blob_service_client.get_blob_client(container=source_container_name, blob=image_name)
        
        try:
            blob_data = blob_client.download_blob().readall()
        except Exception as download_error:
            raise ValueError(f"Failed to download blob '{image_name}' from container '{source_container_name}'. Error: {download_error}")

        try:
            image = Image.open(io.BytesIO(blob_data))
        except Exception as image_error:
            raise ValueError(f"Failed to open image '{image_name}'. Error: {image_error}")

        desired_width = 1280
        min_height = 500
        scale_factor = desired_width / image.width
        new_height = int(image.height * scale_factor)

        if new_height < min_height:
            scale_factor = min_height / image.height
            desired_width = int(image.width * scale_factor)

        resized_image = image.resize((desired_width, int(image.height * scale_factor)), Image.Resampling.LANCZOS)

        output_stream = io.BytesIO()
        resized_image.save(output_stream, format=image.format)
        output_stream.seek(0)

        target_container_name = "resized-images"
        target_blob_name = "resized_" + image_name  

        try:
            blob_client = blob_service_client.get_blob_client(container=target_container_name, blob=target_blob_name)
            blob_client.upload_blob(output_stream, overwrite=True)
        except Exception as upload_error:
            raise ValueError(f"Failed to upload blob '{target_blob_name}' to container '{target_container_name}'. Error: {upload_error}")

        return func.HttpResponse(
            f"Image resized and saved as {target_blob_name} in blob storage.",
            status_code=200
        )
    except ValueError as ve:
        logging.error(f"ValueError: {ve}")
        return func.HttpResponse(str(ve), status_code=400)
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
        return func.HttpResponse(
            f"Unexpected error occurred processing your request. Error: {e}",
            status_code=500
        )

@app.route("maskimage", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def mask_image(req: func.HttpRequest) -> func.HttpResponse:
    try:
        connection_string = "DefaultEndpointsProtocol=https;AccountName=imageworkflow;AccountKey=RvWg7QSEhof25ngK9R9DxUKgfhgcSAEM8jq5p66NQF3gt2uel/9xKffRXC79PAyIkthnMBjZkXcp+AStAV6Kpw==;EndpointSuffix=core.windows.net"
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        image_name = "Steven_Gerrard.jpg" 

        source_container_name = "incoming-images"
        blob_client = blob_service_client.get_blob_client(container=source_container_name, blob=image_name)
        blob_data = blob_client.download_blob().readall()

        face_image = Image.open(io.BytesIO(blob_data))
        img = cv2.cvtColor(np.array(face_image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

        mask_image_path = "batman-mask.png"  
        mask_image = Image.open(mask_image_path).convert("RGBA")

        for (x, y, w, h) in faces:
            if w > 100 and h > 100 and y < gray.shape[0] // 2:
                mask_resized = mask_image.resize((int(w*1.5), int(h*1.5)))
                position = (x - int(0.19 * w), y - int(0.47 * h))
                img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                img_pil.paste(mask_resized, position, mask_resized)
                img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

        final_image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        output_stream = io.BytesIO()
        final_image.save(output_stream, format='JPEG')
        output_stream.seek(0)

        target_container_name = "masked-images"
        target_blob_name = "masked_" + image_name  
        blob_client = blob_service_client.get_blob_client(container=target_container_name, blob=target_blob_name)
        blob_client.upload_blob(output_stream, overwrite=True)

        return func.HttpResponse(
            f"Face mask applied and image saved as {target_blob_name} in blob storage.",
            status_code=200
        )
    except Exception as e:
        logging.exception(e)
        return func.HttpResponse(
            "An error occurred processing your request.",
            status_code=500
        )


@app.route("posterimage", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def poster_image(req: func.HttpRequest) -> func.HttpResponse:
    try:
        connection_string = "DefaultEndpointsProtocol=https;AccountName=imageworkflow;AccountKey=RvWg7QSEhof25ngK9R9DxUKgfhgcSAEM8jq5p66NQF3gt2uel/9xKffRXC79PAyIkthnMBjZkXcp+AStAV6Kpw==;EndpointSuffix=core.windows.net"
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        image_name = "resized_masked_Steven_Gerrard.jpg"  

        source_container_name = "resized-images"
        blob_client = blob_service_client.get_blob_client(container=source_container_name, blob=image_name)
        blob_data = blob_client.download_blob().readall()

        image = Image.open(io.BytesIO(blob_data))

        grayscale_image = image.convert('L')
        poster_image = grayscale_image.convert('RGB')

        draw = ImageDraw.Draw(poster_image)

        font_path = "MEDIO VINTAGE.otf" 
        try:
            font = ImageFont.truetype(font_path, 200)
        except IOError:
            logging.warning("Font file not found, using default font")
            font = ImageFont.load_default()

        text = "THE BATMAN"
        x = (poster_image.width) / 2
        y = poster_image.height - 250 

        draw.text((x, y), text, font=font, fill="yellow", anchor="ms")

        output_stream = io.BytesIO()
        poster_image.save(output_stream, format='JPEG')
        output_stream.seek(0)

        target_container_name = "processed-images"
        target_blob_name = "poster_" + image_name 
        blob_client = blob_service_client.get_blob_client(container=target_container_name, blob=target_blob_name)
        blob_client.upload_blob(output_stream, overwrite=True)

        return func.HttpResponse(
            f"Poster image created and saved as {target_blob_name} in blob storage.",
            status_code=200
        )
    except Exception as e:
        logging.exception(e)
        return func.HttpResponse(
            "An error occurred processing your request.",
            status_code=500
        )
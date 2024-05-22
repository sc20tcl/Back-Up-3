
from PIL import Image
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2

def resize_image(image_path):
    desired_width = 1280
    min_height = 500

    # Load the original image
    img = Image.open(image_path)

    # Calculate scale factor based on desired width
    scale_factor = desired_width / img.width
    new_height = int(img.height * scale_factor)

    # Check if the new height is less than the minimum height
    if new_height < min_height:
        scale_factor = min_height / img.height
        desired_width = int(img.width * scale_factor)

    # Resize the image with the new scale factor
    resized_image = img.resize((desired_width, int(img.height * scale_factor)), Image.Resampling.LANCZOS)

    # Save the resized image before masking
    resized_image_path = image_path.split('.')[0] + '_resized.' + image_path.split('.')[-1]
    resized_image.save(resized_image_path)

    return resized_image_path

def draw_face_boxes_with_mask(image_path, mask_path, size_increase=0.1, position_adjust=(-0.05, -0.1)):
    # Load the image already resized
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

    # Load the Batman mask image with an alpha channel (transparency)
    mask_image = Image.open(mask_path).convert("RGBA")

    # Apply mask to detected faces
    for (x, y, w, h) in faces:
        if w > 50 and h > 50 and y < gray.shape[0] // 2:
            print("*** found****")
            # Resize and position mask
            new_width = int(w * (1 + size_increase))
            new_height = int(h * (1 + size_increase))
            mask_resized = mask_image.resize((new_width, new_height))
            position = (int(x - (new_width - w) * position_adjust[0]), int(y - (new_height - h) * position_adjust[1]))

            # Convert OpenCV image to PIL format and apply mask
            img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            mask_alpha = mask_resized.split()[3]
            img_pil.paste(mask_resized, position, mask_alpha)
            img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    # Save the final image with mask applied
    cv2.imwrite('face-image-with-mask.jpg', img)
    print(f"Processed image saved as face-image.jpg with {len(faces)} face(s) detected.")

def draw_face_boxes(image_path):
    # Load the Haar Cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Read the image from the given path
    img = cv2.imread(image_path)
    
    # Convert the image to grayscale (required for face detection)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, 1.1, 3)
    
    # Draw rectangles around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    # Save the modified image
    cv2.imwrite('face-image.jpg', img)
    print(f"Processed image saved as face-image.jpg with {len(faces)} face(s) detected.")

# Example usage:
resized_image_path = resize_image('Steven_Gerrard.jpg')
draw_face_boxes(resized_image_path)
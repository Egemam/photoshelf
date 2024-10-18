from PIL import Image
import torch
from transformers import OwlViTProcessor, OwlViTForObjectDetection
import os
import concurrent.futures

DEBUG = False
if DEBUG:
    MODEL = "vit-base-patch32"
else:
    MODEL = "vit-large-patch14-336"

if not DEBUG and torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

processor = OwlViTProcessor.from_pretrained("google/owlvit-base-patch32")
model = OwlViTForObjectDetection.from_pretrained("google/owlvit-base-patch32")
model.to(device)

print(device)
def compare_image_with_text(processed_image, img_path, a, th):
    detected = []
    try:
        texts = [[a]]
        inputs = processor(text=texts, images=processed_image, return_tensors="pt")
        outputs = model(**inputs)

        target_sizes = torch.tensor([processed_image.size[::-1]])
        results = processor.post_process_object_detection(outputs=outputs, target_sizes=target_sizes, threshold=th)

        if len(results[0]["labels"]) > 0:
            print("Object detected in the image!\n")
            detected.append(img_path)
        else:
            print("Did not detect the object in the image.\n")
    except Exception as e:
        print(f"Error during text comparison: {e}\n")

    return detected

# Function to manage multiple image processing and comparison tasks
def result(text, mw, th):
    detected = []
    img_dir = "" + os.getcwd() + "\\images"
    fcontent = os.listdir(img_dir)
    image_paths = [os.path.join(img_dir, imag) for imag in fcontent]

    with concurrent.futures.ThreadPoolExecutor(max_workers=mw) as executor:
        futures = []
        for img_path in image_paths:
            # First, process the image without text
            processed_image = Image.open(img_path)
            if processed_image:
                # Then, compare it with the text
                futures.append(executor.submit(compare_image_with_text, processed_image, img_path, text, th))

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                detected.extend(result)
    return detected

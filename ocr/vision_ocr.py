import os
import io
import re
from google.cloud import vision

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:\\miniproj\\ocr\\service_token.json"

client = vision.ImageAnnotatorClient()

ingnored_words=["syp","sgp","tds","cap","caps","days","day","for","sween","hinox","joong","sig"]

# image_path = "C:\\miniproj\\assest\\1.jpg"
def vision_ocr_fn(image_path):
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    
    image = vision.Image(content=content)
    
    response = client.text_detection(image=image)
    texts = response.text_annotations

    filtered_words = []  
    # if texts:
    #     print("Detected Full Text:")
    #     print(texts[0].description)  

    # print("\nFiltered Words (Excluding Digits and Special Characters):")
    for text in texts[1:]:  
        word = text.description
        if re.match("^[A-Za-z]+$", word) and len(word) > 2 and word.lower() not in ingnored_words:  
            filtered_words.append(word)  

    return filtered_words   




# print(filtered_words = vision_ocr_fn(image_path))


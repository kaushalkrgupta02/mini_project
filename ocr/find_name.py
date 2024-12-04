from ocr.med_names import x
from ocr.vision_ocr import vision_ocr_fn

def process_image_and_search(image_path):
    filtered_words = vision_ocr_fn(image_path)

    def search_names(search_word):
        for letter, names in x.items():
            for name in names:
                if search_word.lower() == name.lower():
                    return name
        return None

    med_list = []
    for search_word in filtered_words:
        result = search_names(search_word)
        if result is not None:
            med_list.append(result)

    return med_list


# # Example usage
# image_path = "C:\\miniproj\\assest\\1.jpg"
# final_medicines = process_image_and_search(image_path)
# print(final_medicines)





























# from med_names import x 
# from vision_ocr import vision_ocr_fn

# # here telegram stored photo file path entereed in image_path
# image_path = "C:\\miniproj\\assest\\1.jpg"

# filtered_words = vision_ocr_fn(image_path)

# # print("Filtered Words:", filtered_words)

# def search_names(search_word):
#     # found_names = []
#     for letter, names in x.items():
#         for name in names:
#             if search_word.lower() == name.lower():  
#                 # found_names.append(name)
#                 return name
#     # return found_names

# #new_func ko call karana hai nothing then this
# med_list = []
# def final_list(filtered_words, search_names):
#     for search_word in filtered_words:
#         result = search_names(search_word) 
#         if result != None:
#             med_list.append(result)
#         # if result:
#         # print(f"Found the following names containing '{search_word}':")
#             # for name in result:
#                 # print("ye final hai: ",name)    
#         # else:
#             # print(f"No names found containing '{search_word}'.")
#     # print(med_list)
#     return med_list



# print(final_list(filtered_words, search_names))


import json
import pickle

def get_num_chambers(subcat):
    if subcat == "12-1-1" or subcat == "12-1-2" or subcat == "12-2-1" or subcat == "12-2-2" or subcat=="12-3-1" or subcat=="12-3-2":
        return 1
    elif subcat == "12-1" or subcat=="12-2" or subcat =="12-3":
        return 2
    elif subcat == "12-top" or subcat=="12-bot":
        return 3
    elif subcat == "12-all":
        return 6

def extract_video_links(data):
    image_links = []

    # if isinstance(data, list):
    #     for item in data:
    #         image_links.extend(extract_video_links(item, key))
    # elif isinstance(data, dict):
    #     if key in data:
    #         image_links.append(data[key])
    #     for value in data.values():
    #         image_links.extend(extract_video_links(value, key))
    for item in data:
        if item["speedrun_category"] == "Abyss":
            image_links.append(item["video_link"]+ "\t" +str(get_num_chambers(item["speedrun_subcategory"])))
            print(item["video_link"]+ "\t" +str(get_num_chambers(item["speedrun_subcategory"])))

    return image_links

# Replace 'your_file.json' with the actual path to your JSON file
with open('extract_vidlinks_from_json/tghspeedrunentries.json', 'r', encoding='utf8') as json_file:
    data = json.load(json_file)

# Replace 'image_url' with the key where image links are stored in your JSON
image_links = extract_video_links(data["entries"]["rows"])

with open('extract_vidlinks_from_json/videos.pkl', 'wb') as file:
    pickle.dump(image_links, file)
    print('saved')

# print(image_links)
    

# Download images (same code as previous response)
# import os
# import requests

# # Specify the folder path where you want to save the images
# save_folder = 'I:/Genshin utils app/download-stickers/stickers/'  # Replace 'your_folder_path' with the actual folder path

# # Ensure the folder exists, create it if necessary
# if not os.path.exists(save_folder):
#     os.makedirs(save_folder)
# count = 572
# for i, image_url in enumerate(image_links):
#     try:
#         response = requests.get(image_url)
#         if response.status_code == 200:
#             # Generate a unique filename for each image
#             filename = os.path.join(save_folder, f'image_{count}.jpg')
#             with open(filename, 'wb') as file:
#                 file.write(response.content)
#             print(f"Downloaded {filename}")
#             count+=1
#         else:
#             print(f"Failed to download image from {image_url}")
#     except Exception as e:
#         print(f"Error downloading image_{i}: {str(e)}")


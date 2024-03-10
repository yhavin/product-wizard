"""
Script that uploads a folder of images and returns a CSV
of urls, SKUs, product names, colors, sizes, for batch
uploading to Amazon.

Author: Yakir Havin
"""


import os
import base64
import time

import requests
import pandas as pd
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("API_KEY")
MAX_ATTEMPTS = 5
PARENT_SKU_PREPEND = os.getenv("PARENT_SKU_PREPEND")
PRODUCT_NAME_PREPEND = os.getenv("PRODUCT_NAME_PREPEND")
PRODUCT_NAME_APPEND = "LGBTQ Gay Pride Novelty Hoodie"
SIZE_LIST = ["S", "M", "L", "XL", "2XL", "3XL", "4XL", "5XL"]
CHILD_SKU_CHARS = 8

size_mapping = {value: index for index, value in enumerate(SIZE_LIST)}
files = os.listdir("images")
images = [file for file in files if file.endswith((".png", ".jpg", ".jpeg"))]


def encode(image_path):
    """Encode image as base64 string."""
    with open(image_path, "rb") as image:
        encoded_string = base64.b64encode(image.read()).decode("utf-8")
    return encoded_string

def upload(encoded_image):
    """Upload image to ImgBB."""
    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": API_KEY,
        "image": encoded_image
    }
    response = requests.post(url, data=payload)
    return response.json()

def get_urls():
    """Upload images to ImgBB with retries."""
    start_time = time.time()
    files_and_urls = []
    
    for image in images:
        print("Start:  ", image)
        image_path = os.path.join("images", image)

        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                encoded_image = encode(image_path)
                response = upload(encoded_image)
                
                if response["status"] == 200:
                    print("Success:", image)
                    data = response["data"]
                    url = data["url"]
                    obj = {"filename": image, "url": url}
                    files_and_urls.append(obj)
                    break
                else:
                    print("Fail:   ", image)
                    print(response["status"])
                    print(response["content"])
                    if attempt == MAX_ATTEMPTS:
                        print(f"Final attempt {MAX_ATTEMPTS} failed.")
                    else:
                        print("Retrying...") 
            except Exception as e:
                print(f"Exception on attempt {attempt}: {e}")
                if attempt == MAX_ATTEMPTS:
                    print(f"Final attempt {MAX_ATTEMPTS} failed.")
                else:
                    print("Retrying...") 

    end_time = time.time()
    duration = end_time - start_time  
    print(f"Uploaded {len(files_and_urls)}/{len(images)} images in {duration // 60:.0f}m{duration % 60:.0f}s")

    return files_and_urls 

def create_parent_sku(filename: str):
    """Create parent SKU for a product."""
    # Convert dashes to spaces
    filename_no_dashes = filename.replace("-", " ")

    # Split filename on spaces to get color from end
    filename_split = filename_no_dashes.split(" ")
    color = filename_split[-1][:-4]  # Remove .png extension

    # Remove dashes and spaces
    filename_one_word = filename.replace("-", "").replace(" ", "")
    first_chars = filename_one_word[:CHILD_SKU_CHARS]

    parent_sku = PARENT_SKU_PREPEND + first_chars
    return parent_sku, color

def create_child_sku(parent_sku: str, color: str, size: str):
    """Create child SKU for a product."""
    return f"{parent_sku}-{color}-{size}"

def add_skus(lst: list):
    """Return child SKU rows using color and size combinations."""
    all_child_sku_elements = []

    for parent_element in lst:
        filename = parent_element["filename"]
        parent_sku, color = create_parent_sku(filename)
        parent_element["parent_sku"] = parent_sku

        this_child_sku_elements = []
        for size in SIZE_LIST:
            child_sku_element = parent_element.copy()
            child_sku = create_child_sku(parent_sku, color, size)
            child_sku_element["child_sku"] = child_sku
            child_sku_element["color"] = color
            child_sku_element["size"] = size
            this_child_sku_elements.append(child_sku_element)

        all_child_sku_elements.extend(this_child_sku_elements)
    return all_child_sku_elements

def create_product_name(product_object: dict):
    """Create product name for a product."""
    filename_no_dashes = product_object["filename"].replace("-", " ")
    filename_split = filename_no_dashes.split(" ")
    color = product_object["color"]
    product = " ".join(filename_split[:-1])
    product_upper = product.title()
    size = product_object["size"]
    product_name = f"{PRODUCT_NAME_PREPEND} {product_upper} {PRODUCT_NAME_APPEND}, {color}, {size}"
    return product_name

def main():
    """Main driver function."""
    files_and_urls = get_urls()
    products_with_skus = add_skus(files_and_urls)
    for product in products_with_skus:
        product["product_name"] = create_product_name(product)
    products_with_skus = sorted(products_with_skus, key=lambda product: (product["filename"], size_mapping[product["size"]]))
    df = pd.DataFrame(products_with_skus)
    csv_path = f"on_coast_products_{int(time.time())}.csv"
    df.to_csv(csv_path, index=False)
    print("Saved to", csv_path)


main()
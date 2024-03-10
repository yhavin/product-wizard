"""
Streamlit app for uploading images and returning a CSV with
urls, SKUs, product names, colors, sizes, for batch
uploading to Amazon.

Author: Yakir Havin
"""


import base64
import time
from datetime import datetime

import streamlit as st
import requests
import pandas as pd


st.set_page_config(page_title="Product Wizard", page_icon="👕")
st.title("Amazon Product Wizard")
st.caption("Developed by Yakir Havin")

# Form input setup and constant declarations
MAX_ATTEMPTS = 5
form = st.form(key="input-form")
images = form.file_uploader("Upload images", accept_multiple_files=True, type=["png", "jpg"])
form.info("Note: Image filenames must end with color preceded by space or hyphen, e.g., 'Zen Ramen Bowl T-Shirt Blue.png'")
API_KEY = form.text_input("API key", value="8c14c34665298adb85a1b59a841fb72b").strip()
PARENT_SKU_PREFIX = form.text_input("Parent SKU prefix", placeholder="e.g., SH, TNK, HDIE").strip()
PRODUCT_NAME_PREFIX = form.text_input("Product name prefix", value="On Coast").strip()
PRODUCT_NAME_APPEND = form.text_input("Product name appended words", placeholder="e.g., Celebratory Novelty T-Shirt").strip()
size_list_options = ["S", "M", "L", "XL", "2XL", "3XL", "4XL", "5XL"]
SIZE_LIST = form.multiselect("Sizes", options=size_list_options, default=size_list_options)
size_mapping = {value: index for index, value in enumerate(SIZE_LIST)}
CHILD_SKU_CHARS = form.number_input("Child SKU characters", min_value=6, max_value=12, value=8)

submit = form.form_submit_button("Submit")

############################################

def encode(image):
    """Encode image as base64 string."""
    image_bytes = image.getvalue()
    encoded_string = base64.b64encode(image_bytes).decode("utf-8")
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
    """Upload images to ImgBB with retries, and display progress."""
    start_time = time.time()
    files_and_urls = []

    status_window = st.status("🪄 Working some magic...")
    
    for i in range(len(images)):
        image = images[i]
        image_name = image.name
        print("Start:  ", image_name)

        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                encoded_image = encode(image)
                response = upload(encoded_image)
                
                if response["status"] == 200:
                    print("Success:", image_name)
                    data = response["data"]
                    url = data["url"]
                    obj = {"filename": image_name, "url": url}
                    files_and_urls.append(obj)
                    status_window.write(image_name)
                    break
                else:
                    print("Fail:   ", image_name)
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
    completion_text = f"Uploaded {len(files_and_urls)}/{len(images)} images in {duration // 60:.0f} minutes, {duration % 60:.0f} seconds"
    print(completion_text)

    if len(files_and_urls) == len(images):
        st.success(completion_text)
    elif len(files_and_urls) < len(images):
        st.warning(completion_text)
    else:
        st.info(completion_text)

    status_window.update(label="✨ Ready for download", state="complete")

    return files_and_urls 

def create_parent_sku(filename: str):
    """Create parent SKU for a product."""
    # Convert dashes to spaces
    filename_no_dashes = filename.replace("-", " ")

    # Split filename on spaces to get color from end
    filename_split = filename_no_dashes.split(" ")
    color = filename_split[-1][:-4].title()  # Remove .png extension and capitalise

    # Remove dashes and spaces
    filename_one_word = filename.replace("-", "").replace(" ", "")
    first_chars = filename_one_word[:CHILD_SKU_CHARS].upper()

    parent_sku = f"{PARENT_SKU_PREFIX}-{first_chars}"
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
    product_name = f"{PRODUCT_NAME_PREFIX} {product_upper} {PRODUCT_NAME_APPEND}, {color}, {size}"
    return product_name

def display_download_button(df: pd.DataFrame):
    """Display DataFrame and download button."""
    csv = df.to_csv(index=False).encode("utf-8")
    output_file_name = f"products_{datetime.today().strftime('%Y%m%d_%H%M%S')}.csv"
    st.download_button("Download CSV", data=csv, file_name=output_file_name, mime="text/csv", type="primary", key="download-top")
    st.dataframe(df, height=35 * len(df) + 3, hide_index=True)
    st.download_button("Download CSV", data=csv, file_name=output_file_name, mime="text/csv", type="primary", key="download-bottom")
type="primary", 
def main():
    """Main driver function."""
    files_and_urls = get_urls()
    products_with_skus = add_skus(files_and_urls)
    for product in products_with_skus:
        product["product_name"] = create_product_name(product)
    products_with_skus = sorted(products_with_skus, key=lambda product: (product["filename"], size_mapping[product["size"]]))
    df = pd.DataFrame(products_with_skus)
    display_download_button(df)

if submit:
    main()
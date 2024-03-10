# Amazon product wizard

Using a folder of images, return a CSV with image URLs, product names, parent and child SKUs, colors, and sizes.

Perfect for bulk uploading listings using the Amazon template.

## Quick start
1. Download `main.py`.
2. Install required libraries.
```python
$ pip install -r requirements.txt
```
3. Add images to a sibling folder named `images`.
4. Add your ImgBB API key to a `.env` file.
5. Set your constant variables at the beginning of the module.
6. Run module.
7. CSV is output to working directory.
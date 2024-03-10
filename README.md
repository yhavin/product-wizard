# Amazon product wizard

Using a folder of images, return a CSV with image URLs, product names, parent and child SKUs, colors, and sizes.

Perfect for bulk uploading listings using the Amazon template.

## Quick start
1. Download `local.py`.
2. Install required libraries.
```shell
$ pip install -r requirements.txt
```
3. Add images to a sibling folder named `images`.
4. Add your ImgBB API key to a `.env` file.
5. Set your constant variables at the beginning of the module.
6. Run `local.py` module.
7. CSV is output to working directory, sorted by filename then size.

## Example
List of image files
```
CALM T-SHIRT BLACK.png,
HYPER T-SHIRT BLUE.png,
ZEN MODE GALAXY SHIRT GREY.png,
ST PATRICK'S DAY LUCKY CLOVER T-SHIRT GREEN.png
```

CSV
| filename                                          | url     | parent_sku  | child_sku             | color | size | product_name                                                      |
|---------------------------------------------------|---------|-------------|-----------------------|-------|------|-------------------------------------------------------------------|
| CALM T-SHIRT BLACK.png                            | \<url\> | SH-CALMTSHI | SH-CALMTSHI-BLACK-S   | BLACK | S    | Calm T Shirt Novelty T-Shirt, BLACK, S                            |
| CALM T-SHIRT BLACK.png                            | \<url\> | SH-CALMTSHI | SH-CALMTSHI-BLACK-M   | BLACK | M    | Calm T Shirt Novelty T-Shirt, BLACK, M                            |
| CALM T-SHIRT BLACK.png                            | \<url\> | SH-CALMTSHI | SH-CALMTSHI-BLACK-L   | BLACK | L    | Calm T Shirt Novelty T-Shirt, BLACK, L                            |
| CALM T-SHIRT BLACK.png                            | \<url\> | SH-CALMTSHI | SH-CALMTSHI-BLACK-XL  | BLACK | XL   | Calm T Shirt Novelty T-Shirt, BLACK, XL                           |
| CALM T-SHIRT BLACK.png                            | \<url\> | SH-CALMTSHI | SH-CALMTSHI-BLACK-2XL | BLACK | 2XL  | Calm T Shirt Novelty T-Shirt, BLACK, 2XL                          |
| CALM T-SHIRT BLACK.png                            | \<url\> | SH-CALMTSHI | SH-CALMTSHI-BLACK-3XL | BLACK | 3XL  | Calm T Shirt Novelty T-Shirt, BLACK, 3XL                          |
| CALM T-SHIRT BLACK.png                            | \<url\> | SH-CALMTSHI | SH-CALMTSHI-BLACK-4XL | BLACK | 4XL  | Calm T Shirt Novelty T-Shirt, BLACK, 4XL                          |
| CALM T-SHIRT BLACK.png                            | \<url\> | SH-CALMTSHI | SH-CALMTSHI-BLACK-5XL | BLACK | 5XL  | Calm T Shirt Novelty T-Shirt, BLACK, 5XL                          |
| HYPER T-SHIRT BLUE.png                            | \<url\> | SH-HYPERTSH | SH-HYPERTSH-BLUE-S    | BLUE  | S    | Hyper T Shirt Novelty T-Shirt, BLUE, S                            |
| HYPER T-SHIRT BLUE.png                            | \<url\> | SH-HYPERTSH | SH-HYPERTSH-BLUE-M    | BLUE  | M    | Hyper T Shirt Novelty T-Shirt, BLUE, M                            |
| HYPER T-SHIRT BLUE.png                            | \<url\> | SH-HYPERTSH | SH-HYPERTSH-BLUE-L    | BLUE  | L    | Hyper T Shirt Novelty T-Shirt, BLUE, L                            |
| HYPER T-SHIRT BLUE.png                            | \<url\> | SH-HYPERTSH | SH-HYPERTSH-BLUE-XL   | BLUE  | XL   | Hyper T Shirt Novelty T-Shirt, BLUE, XL                           |
| HYPER T-SHIRT BLUE.png                            | \<url\> | SH-HYPERTSH | SH-HYPERTSH-BLUE-2XL  | BLUE  | 2XL  | Hyper T Shirt Novelty T-Shirt, BLUE, 2XL                          |
| HYPER T-SHIRT BLUE.png                            | \<url\> | SH-HYPERTSH | SH-HYPERTSH-BLUE-3XL  | BLUE  | 3XL  | Hyper T Shirt Novelty T-Shirt, BLUE, 3XL                          |
| HYPER T-SHIRT BLUE.png                            | \<url\> | SH-HYPERTSH | SH-HYPERTSH-BLUE-4XL  | BLUE  | 4XL  | Hyper T Shirt Novelty T-Shirt, BLUE, 4XL                          |
| HYPER T-SHIRT BLUE.png                            | \<url\> | SH-HYPERTSH | SH-HYPERTSH-BLUE-5XL  | BLUE  | 5XL  | Hyper T Shirt Novelty T-Shirt, BLUE, 5XL                          |
| ST PATRICK'S DAY LUCKY CLOVER T-SHIRT   GREEN.png | \<url\> | SH-STPATRIC | SH-STPATRIC-GREEN-S   | GREEN | S    | St Patrick'S Day Lucky Clover T Shirt Novelty T-Shirt, GREEN, S   |
| ST PATRICK'S DAY LUCKY CLOVER T-SHIRT   GREEN.png | \<url\> | SH-STPATRIC | SH-STPATRIC-GREEN-M   | GREEN | M    | St Patrick'S Day Lucky Clover T Shirt Novelty T-Shirt, GREEN, M   |
| ST PATRICK'S DAY LUCKY CLOVER T-SHIRT   GREEN.png | \<url\> | SH-STPATRIC | SH-STPATRIC-GREEN-L   | GREEN | L    | St Patrick'S Day Lucky Clover T Shirt Novelty T-Shirt, GREEN, L   |
| ST PATRICK'S DAY LUCKY CLOVER T-SHIRT   GREEN.png | \<url\> | SH-STPATRIC | SH-STPATRIC-GREEN-XL  | GREEN | XL   | St Patrick'S Day Lucky Clover T Shirt Novelty T-Shirt, GREEN, XL  |
| ST PATRICK'S DAY LUCKY CLOVER T-SHIRT   GREEN.png | \<url\> | SH-STPATRIC | SH-STPATRIC-GREEN-2XL | GREEN | 2XL  | St Patrick'S Day Lucky Clover T Shirt Novelty T-Shirt, GREEN, 2XL |
| ST PATRICK'S DAY LUCKY CLOVER T-SHIRT   GREEN.png | \<url\> | SH-STPATRIC | SH-STPATRIC-GREEN-3XL | GREEN | 3XL  | St Patrick'S Day Lucky Clover T Shirt Novelty T-Shirt, GREEN, 3XL |
| ST PATRICK'S DAY LUCKY CLOVER T-SHIRT   GREEN.png | \<url\> | SH-STPATRIC | SH-STPATRIC-GREEN-4XL | GREEN | 4XL  | St Patrick'S Day Lucky Clover T Shirt Novelty T-Shirt, GREEN, 4XL |
| ST PATRICK'S DAY LUCKY CLOVER T-SHIRT   GREEN.png | \<url\> | SH-STPATRIC | SH-STPATRIC-GREEN-5XL | GREEN | 5XL  | St Patrick'S Day Lucky Clover T Shirt Novelty T-Shirt, GREEN, 5XL |
| ZEN MODE GALAXY SHIRT GREY.png                    | \<url\> | SH-ZENMODEG | SH-ZENMODEG-GREY-S    | GREY  | S    | Zen Mode Galaxy Shirt Novelty T-Shirt, GREY, S                    |
| ZEN MODE GALAXY SHIRT GREY.png                    | \<url\> | SH-ZENMODEG | SH-ZENMODEG-GREY-M    | GREY  | M    | Zen Mode Galaxy Shirt Novelty T-Shirt, GREY, M                    |
| ZEN MODE GALAXY SHIRT GREY.png                    | \<url\> | SH-ZENMODEG | SH-ZENMODEG-GREY-L    | GREY  | L    | Zen Mode Galaxy Shirt Novelty T-Shirt, GREY, L                    |
| ZEN MODE GALAXY SHIRT GREY.png                    | \<url\> | SH-ZENMODEG | SH-ZENMODEG-GREY-XL   | GREY  | XL   | Zen Mode Galaxy Shirt Novelty T-Shirt, GREY, XL                   |
| ZEN MODE GALAXY SHIRT GREY.png                    | \<url\> | SH-ZENMODEG | SH-ZENMODEG-GREY-2XL  | GREY  | 2XL  | Zen Mode Galaxy Shirt Novelty T-Shirt, GREY, 2XL                  |
| ZEN MODE GALAXY SHIRT GREY.png                    | \<url\> | SH-ZENMODEG | SH-ZENMODEG-GREY-3XL  | GREY  | 3XL  | Zen Mode Galaxy Shirt Novelty T-Shirt, GREY, 3XL                  |
| ZEN MODE GALAXY SHIRT GREY.png                    | \<url\> | SH-ZENMODEG | SH-ZENMODEG-GREY-4XL  | GREY  | 4XL  | Zen Mode Galaxy Shirt Novelty T-Shirt, GREY, 4XL                  |
| ZEN MODE GALAXY SHIRT GREY.png                    | \<url\> | SH-ZENMODEG | SH-ZENMODEG-GREY-5XL  | GREY  | 5XL  | Zen Mode Galaxy Shirt Novelty T-Shirt, GREY, 5XL                  |
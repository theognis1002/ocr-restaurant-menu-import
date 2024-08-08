# OCR Image Menu Text Extractor

## Overview

This script extracts text from images of restaurant menus using Optical Character Recognition (OCR) and then enhances and structures the extracted text using a language model. The script processes images in a specified directory and outputs the structured data to a JSON file.

## Features

- **OCR Extraction**: Uses `pytesseract` to extract text from images.
- **Text Enhancement**: Utilizes a language model (`litellm`) to convert raw text into structured JSON.
- **Multiprocessing**: Processes multiple images in parallel to improve performance.
- **Supports Multiple Formats**: Handles various image formats such as JPEG, PNG, BMP, and TIFF.

## Requirements

- Python 3.12
- `pytesseract`
- `Pillow` (PIL)
- `litellm`
- `multiprocessing` (part of Python standard library)

You can install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

## Configuration

- `IMAGES_DIR`: Directory where the images are located (default: `images/`).
- `OUTPUT_FILE`: File where the structured JSON data will be saved (default: `output.json`).

## Usage

1. Place the script in your desired directory.
2. Ensure your images are located in the directory specified by `IMAGES_DIR`.
3. `pip install -r requirements.txt`
4. `python main.py`

## Script Details

### Functions

- `extract_text(image_path: str) -> str`: Extracts text from the specified image using OCR.
- `enhance_and_jsonify_text(raw_text: str) -> dict`: Enhances raw text and converts it into structured JSON using a language model.
- `process_image(image_file: Path) -> dict`: Processes a single image file and returns the result as a dictionary.
- `process_images_from_directory(directory_path: str) -> dict`: Processes all images in the given directory using multiprocessing.
- `main(directory_path: str, output_file: str) -> None`: Main function to process images and write results to a JSON file.

## 📜 License

Distributed under the MIT License. See [`LICENSE`](./LICENSE) for more information.

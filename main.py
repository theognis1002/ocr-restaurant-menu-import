import json
import logging
from multiprocessing import Pool, cpu_count
from pathlib import Path

import litellm
import pytesseract
from PIL import Image

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger()
IMAGES_DIR = "images/"
OUTPUT_FILE = "output.json"

SAMPLE_SCHEMA = {
    "categories": [
        {
            "name": "Seafood",
            "description": "Various seafood dishes",
            "slug": "seafood",
            "is_active": True,
        },
        {
            "name": "Chef's Specialties",
            "description": "Specialty dishes prepared by the chef",
            "slug": "chefs-specialties",
            "is_active": True,
        },
        {
            "name": "Noodles",
            "description": "Various noodle dishes",
            "slug": "noodles",
            "is_active": True,
        },
    ],
    "products": [
        {
            "title": "Shrimp with Broccoli",
            "price_excl_tax": "14.45",
            "price_incl_tax": "14.45",
            "category": "Seafood",
            "description": "Shrimp with broccoli",
            "is_active": True,
        },
        {
            "title": "Shrimp with Chinese Vegetables",
            "price_excl_tax": "14.45",
            "price_incl_tax": "14.45",
            "category": "Seafood",
            "description": "Shrimp with Chinese vegetables",
            "is_active": True,
        },
    ],
}


def extract_text(image_path: str) -> str:
    """Extract text from an image using OCR."""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    LOGGER.info(f"Extracted text from {image_path}: {text}")
    return text


def enhance_and_jsonify_text(raw_text: str) -> dict:
    """Use an LLM to enhance and convert raw text into structured JSON."""
    messages = [
        {
            "role": "system",
            "content": f"Return an array of JSON objects ONLY using the raw menu text that is incoming from OCR of images of a Chinese restaurant menu.\nHere is an example schema: {json.dumps(SAMPLE_SCHEMA)}",
        },
        {
            "role": "user",
            "content": f"OCR raw text: {raw_text}",
        },
    ]
    response = litellm.completion(
        model="gpt-4o-mini",
        temperature=0,
        response_format={"type": "json_object"},
        messages=messages,
    )
    choice = response.choices[0]
    return json.loads(choice.message.content)


def process_image(image_file: Path) -> dict:
    """Process a single image file and return the result as a dictionary."""
    raw_text = extract_text(image_file)
    try:
        json_data = enhance_and_jsonify_text(raw_text)
        LOGGER.info(f"Processed data for {image_file.name}: {json_data}")
    except Exception as excp:
        LOGGER.error(f"Error processing {image_file.name}: {str(excp)}")
        json_data = None

    return {"file": image_file.name, "data": json_data}


def process_images_from_directory(directory_path: str) -> dict:
    """Process all images in the given directory and compile results into a JSON object using multiprocessing."""
    results = []
    image_files = list(Path(directory_path).glob("*.jpg"))

    # Use multiprocessing to process images in parallel
    with Pool(cpu_count()) as pool:
        results = pool.map(process_image, image_files)

    return results


def main(directory_path: str, output_file: str) -> None:
    """Main function to process images and write results to a JSON file."""
    results = process_images_from_directory(directory_path)
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)

    LOGGER.info(f"Successfully wrote results to {output_file}")


if __name__ == "__main__":
    main(IMAGES_DIR, OUTPUT_FILE)

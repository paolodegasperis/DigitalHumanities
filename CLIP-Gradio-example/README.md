
# Image Similarity Finder

This project is a Gradio-based interface that allows users to input text and retrieve the three most similar images from a set of image embeddings. It utilizes the CLIP model to compute text-image similarity using cosine similarity.

## Features

- Uses the CLIP model (`laion/CLIP-ViT-L-14-laion2B-s32B-b82K`) for text-image comparison.
- Returns the three most similar images to the input text.
- Displays a gallery of similar images and their corresponding similarity scores.
- Built with Gradio for an easy-to-use interface.

## Requirements

- Python 3.x
- Gradio
- PyTorch
- Transformers
- Scikit-learn
- PIL
- Pandas

You can install the dependencies using the following command:

```bash
pip install gradio torch transformers scikit-learn pillow pandas
```

## How to Run

1. Clone the repository or download the code.
2. Place your image embeddings in a CSV file (replace the path `embeddings.csv` in the code with the correct path). The first column should contain the image filenames, and the rest of the columns should contain the image embeddings.
3. Ensure you have a folder named `img` containing the images referenced in the CSV file.
4. Run the `app.py` script:

```bash
python app.py
```

The application will launch a Gradio interface in your browser.

## How It Works

1. The CLIP model is loaded using the `load_clip_model` function.
2. Image embeddings are loaded from a CSV file using the `load_embeddings` function.
3. When a user inputs text, the `query_images` function generates a text embedding, compares it to the image embeddings using cosine similarity, and returns the three most similar images.
4. The images and their similarity scores are displayed in the Gradio interface.

## File Structure

- `app.py`: Main application file.
- `embeddings.csv`: CSV file containing image embeddings (replace with your own).
- `img/`: Directory containing the images referenced in the CSV file.

## Credits

This project utilizes the CLIP model from Hugging Face and Gradio for the interface.

import base64
import os

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

#reads an image file from a given path and encodes it into a base64 string
def encode_image(image_path):
    """Getting the base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

''' Function takes a base64-encoded image and a prompt as input. It initializes a chat session 
    with the GPT-4 Vision model and constructs a message containing both the prompt and the image URL 
    encoded in base64 format
'''
def image_summarize(img_base64, prompt):
    """Make image summary"""
    chat = ChatOpenAI(model="gpt-4o", max_tokens=200)

    msg = chat.invoke(
        [
            HumanMessage(
                content=[
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"},
                    },
                ]
            )
        ]
    )
    return msg.content

''' Function processes a directory containing JPEG images. It iterates through each image file,
    encoding it into base64 format, and generating a summary using the image_summarize function.


    A prompt is defined within the generate_img_summaries function, instructing the assistant to provide concise summaries optimized for retrieval
'''
def generate_img_summaries(path):
    """
    Generate summaries and base64 encoded strings for images
    path: Path to list of .jpg files extracted by Unstructured
    """

    # Store base64 encoded images
    img_base64_list = []

    # Store image summaries
    image_summaries = []

    # Prompt
    from tqdm import tqdm
    import time

    prompt = """You are an assistant tasked with summarizing images for retrieval. \
        These summaries will be embedded and used to retrieve the raw image. \
        Give a concise summary of the image that is well optimized for retrieval."""

    count = 0

    for img_file in tqdm(sorted(os.listdir(path)), desc="Processing images"):
        if img_file.endswith(".jpg"):
            img_path = os.path.join(path, img_file)

            try:
                base64_image = encode_image(img_path)
                img_base64_list.append(base64_image)
                image_summaries.append(image_summarize(base64_image, prompt))
                count += 1

            except Exception as e:
                print(f"Error processing image {img_file}: {e}")

    return img_base64_list, image_summaries

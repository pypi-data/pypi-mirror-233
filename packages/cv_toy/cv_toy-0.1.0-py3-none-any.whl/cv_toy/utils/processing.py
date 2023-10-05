import cv2
import numpy as np
import requests
from io import BytesIO

def load_image(image_source):
    """
    Load an image from either a local file path or a URL.

    Parameters:
    - image_source: Either a local file path or a URL to the image.

    Returns:
    - image: The loaded image as a NumPy array.
    - success: A boolean indicating whether the image loading was successful.
    """

    # Check if image_source is a URL
    if image_source.startswith(('http://', 'https://')):
        try:
            response = requests.get(image_source)
            if response.status_code == 200:
                image_bytes = BytesIO(response.content)
                image = cv2.imdecode(np.asarray(bytearray(image_bytes.read()), dtype=np.uint8), cv2.IMREAD_COLOR)[:,:,::-1]
                return image, True
            else:
                print(f"Failed to fetch image from URL. Status code: {response.status_code}")
                return None, False
        except Exception as e:
            print(f"Error loading image from URL: {str(e)}")
            return None, False

    # Otherwise, assume image_source is a local file path
    else:
        try:
            image = cv2.imread(image_source, cv2.COLOR_BGR2RGB)
            if image is not None:
                return image, True
            else:
                print(f"Failed to load image from local path: {image_source}")
                return None, False
        except Exception as e:
            print(f"Error loading image from local path: {str(e)}")
            return None, False



# Example usage:
# image, success = load_image('local_image.jpg')
# image, success = load_image('https://example.com/remote_image.jpg')

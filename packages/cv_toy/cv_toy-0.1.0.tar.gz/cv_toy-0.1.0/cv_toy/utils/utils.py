import numpy as np
from skimage.util import img_as_float, img_as_ubyte

def add_noise(image, noise_type='gaussian', intensity=0.1):
    """
    Add noise to an input image.

    Parameters:
    - image: The input image (numpy.ndarray) to which noise will be added.
    - noise_type: Type of noise to add. Supported types are 'gaussian', 'salt_and_pepper', and 'speckle'.
    - intensity: The intensity of noise to add. A higher value increases the intensity of the noise.

    Returns:
    - noisy_image: The image with added noise.
    """
    to_type = img_as_ubyte if image.max() > 1 else img_as_float
    noisy_image = img_as_float(image.copy())

    if noise_type == 'gaussian':
        gaussian_noise = np.random.normal(0, 1., image.shape)
        noisy_image += intensity * gaussian_noise

    elif noise_type == 'salt_and_pepper':
        noise_mask = np.random.rand(*image.shape)
        noisy_image[noise_mask < intensity / 2] = 0  # Salt noise
        noisy_image[noise_mask > 1 - intensity / 2] = 1.  # Pepper noise

    elif noise_type == 'speckle':
        speckle_noise = np.random.normal(0, intensity, image.shape)
        noisy_image += noisy_image * speckle_noise

    else:
        raise ValueError("Unsupported noise type. Use 'gaussian', 'salt_and_pepper', or 'speckle'.")

    noisy_image = np.clip(noisy_image, 0, 1.)

    return to_type(noisy_image)

from typing import Tuple
import cv2
import numpy as np


Bounds = Tuple[int, int, int, int]
Color = Tuple[int, int, int]

COLOR_RED: Color = (255, 0, 0)
COLOR_BLACK: Color = (0, 0, 0)

def cut_patch(image: np.ndarray, 
              bounds: Bounds) -> np.ndarray:
    """
    Cuts a patch from the input image based on the provided bounds.
    
    Args:
        image (np.ndarray): The input image.
        bounds (Bounds): Bounds for cropping (top, bottom, left, right).
    
    Returns:
        np.ndarray: The cropped patch.
    """
    assert len(bounds) == 4, 'Check the bounds'
    return image[bounds[0]:bounds[1], bounds[2]:bounds[3], ...]

def draw_rectangle(image: np.ndarray, 
                   bounds: Bounds, 
                   thickness: int=2,
                   color: Color=COLOR_RED) -> np.ndarray:
    """
    Draws a rectangle on the input image based on the provided bounds.
    
    Args:
        image (np.ndarray): The input image.
        bounds (Bounds): Bounds for the rectangle (top, bottom, left, right).
        thickness (int): Thickness of the rectangle's border.
    
    Returns:
        np.ndarray: The image with the drawn rectangle.
    """
    assert len(bounds) == 4, 'Check the bounds'
    start_point = (bounds[3], bounds[1])
    end_point = (bounds[2], bounds[0])
    with_rectangle = cv2.rectangle(image.copy(), 
                                   start_point, 
                                   end_point, 
                                   color, thickness)
    return with_rectangle

def color_overlap(patch: np.ndarray, 
                  scale: Tuple[float, float], 
                  thickness: int, 
                  color: Tuple[int, int, int]=COLOR_RED) -> np.ndarray:
    """
    Adds a colored border around a patch based on the specified scale and thickness.
    
    Args:
        patch (np.ndarray): The input patch.
        scale (Tuple[float, float]): Scaling factors for height and width.
        thickness (int): Thickness of the colored border.
        color (Tuple[int, int, int]): RGB color for the border.
    
    Returns:
        np.ndarray: The patch with the colored border.
    """
    h, w, c = patch.shape
    h = h + int(h * scale[0])
    w = w + int(w * scale[1])
    resized_patch = cv2.resize(patch.copy(), (w, h))
    
    overlapped = np.zeros((h + 2 * thickness, w + 2 * thickness, c))
    overlapped[thickness:-thickness, thickness:-thickness, ...] = resized_patch
    overlapped[:thickness, :, ...] = overlapped[:, :thickness, ...] = \
        overlapped[-thickness:, :, ...] = overlapped[:, -thickness:, ...] = color

    return overlapped

def position_handler(image: np.ndarray, 
                     overlapped: np.ndarray, 
                     position: str) -> np.ndarray:
    """
    Handles the placement of the overlapped patch on the input 
    image based on the specified position.
    
    Args:
        image (np.ndarray): The input image.
        overlapped (np.ndarray): The overlapped patch with the colored border.
        position (str): Position for adding the colored border. 
            Options: "top_left", "top_right", "bottom_left", "bottom_right",
                "center_top", "center_bottom", "center_left", "center_right".
    
    Returns:
        np.ndarray: The image with the overlapped patch at the specified position.
    """
    rect_h, rect_w, _ = image.shape
    h, w, c = overlapped.shape
    
    if position == "top_left":
        image[:h, :w, ...] = overlapped
    elif position == "top_right":
        image[:h, -w:, ...] = overlapped
    elif position == "bottom_left":
        image[-h:, :w, ...] = overlapped
    elif position == "bottom_right":
        image[-h:, -w:, ...] = overlapped
    elif position == "center_top":
        x_center = rect_w // 2
        x_start = x_center - w // 2
        x_end = x_start + w
        image[:h, x_start:x_end, ...] = overlapped
    elif position == "center_bottom":
        x_center = rect_w // 2
        x_start = x_center - w // 2
        x_end = x_start + w
        image[-h:, x_start:x_end, ...] = overlapped
    elif position == "center_left": 
        y_center = rect_h // 2
        y_start = y_center - h // 2
        y_end = y_start + h
        image[y_start:y_end, :w, ...] = overlapped
    elif position == "center_right": 
        y_center = rect_h // 2
        y_start = y_center - h // 2
        y_end = y_start + h
        image[y_start:y_end, -w:, ...] = overlapped    
    else:
        raise ValueError("Invalid position. Supported positions: \
                         'top_left', 'top_right', 'bottom_left', 'bottom_right', \
                         'center_top', 'center_bottom', 'center_left', 'center_right'")
    
    return image



def cut_add_patch(image: np.ndarray, 
                  bounds: Bounds, 
                  thickness: int=2,
                  max_scale: float=0.3,
                  position: str="bottom_right",
                  rotation_direction: str=None,
                  transpose: bool=False,
                  color: Color=COLOR_RED) -> np.ndarray:
    """
    Cuts a patch, draws a rectangle, and adds a colored border 
    to the input image with adaptive scaling and rotation.
    
    Args:
        image (np.ndarray): The input image.
        bounds (Bounds): Bounds for cropping (top, bottom, left, right).
        thickness (int): Thickness of the rectangle's border and the colored border.
        max_scale (float): Maximum scaling factor for the patch. 
            Should be between 0 and 1.
        position (str): Position for adding the colored border. 
            Options: "top_left", "top_right", "bottom_left", "bottom_right",
            "center_top", "center_bottom", "center_left", "center_right".
        rotation_direction (str): Direction of rotation. 
            Options: "clockwise" or "counterclockwise".
    
    Returns:
        np.ndarray: The modified image.
    """
    assert len(bounds) == 4, 'Check the bounds'
    image = image.transpose((1, 0, 2)) if transpose else image
    patch = cut_patch(image, bounds)
    with_rectangle = draw_rectangle(image, bounds, thickness, color)
    
    patch_h, patch_w, _ = patch.shape
    rect_h, rect_w, _ = with_rectangle.shape
    
    scale_h = max_scale * rect_h / patch_h
    scale = (scale_h, scale_h)
    
    overlapped = color_overlap(patch, scale=scale, thickness=thickness)
    if rotation_direction == "clockwise":
        overlapped = cv2.transpose(overlapped)
        overlapped = cv2.flip(overlapped, flipCode=1)  # Horizontal flip
    elif rotation_direction == "counterclockwise":
        overlapped = cv2.transpose(overlapped)
        overlapped = cv2.flip(overlapped, flipCode=0)  # Vertical flip
    return position_handler(with_rectangle, overlapped, position)
import os
import numpy as np
from PIL import Image
import imageio
from skimage.color import rgb2gray
from skimage.feature import canny
from skimage.morphology import dilation, square
from scipy import ndimage as ndi
from skimage.measure import label, regionprops
from skimage.draw import rectangle_perimeter

def save_image(array, path, mode='L'):
    """Save a NumPy array as an image."""
    img = Image.fromarray((array * 255).astype(np.uint8)) if array.dtype != np.uint8 else Image.fromarray(array)
    if mode == 'RGB':
        img = img.convert('RGB')
    img.save(path)

def segment_panels(image_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Load image
    image = imageio.imread(image_path)
    save_image(image, os.path.join(output_dir, 'original.png'), mode='RGB')

    # Convert to grayscale
    # Remove alpha channel if present
    if image.shape[-1] == 4:
        image = image[..., :3]

    # Convert to grayscale
    gray = rgb2gray(image)
    save_image(gray, os.path.join(output_dir, 'grayscale.png'))

    save_image(gray, os.path.join(output_dir, 'grayscale.png'))

    # Apply Canny edge detection
    edges = canny(gray)
    save_image(edges, os.path.join(output_dir, 'edges.png'))

    # Dilate edges to close gaps
    thick_edges = dilation(edges, square(3))
    thick_edges = dilation(thick_edges, square(3))
    save_image(thick_edges, os.path.join(output_dir, 'dilated_edges.png'))

    # Fill holes to create solid panel regions
    filled = ndi.binary_fill_holes(thick_edges)
    save_image(filled, os.path.join(output_dir, 'filled.png'))

    # Label connected regions and draw boxes
    label_image = label(filled)
    labeled_image = np.zeros_like(image)
    for region in regionprops(label_image):
        minr, minc, maxr, maxc = region.bbox
        rr, cc = rectangle_perimeter(start=(minr, minc), end=(maxr, maxc), shape=label_image.shape)
        labeled_image[rr, cc] = [255, 0, 0]  # Red box
    save_image(labeled_image, os.path.join(output_dir, 'labeled.png'), mode='RGB')

    # Extract and save individual panels
    panel_dir = os.path.join(output_dir, 'panels')
    os.makedirs(panel_dir, exist_ok=True)
    panel_count = 0
    for region in regionprops(label_image):
        minr, minc, maxr, maxc = region.bbox
        if (maxr - minr) * (maxc - minc) < 1000:
            continue  # Skip very small regions
        panel = image[minr:maxr, minc:maxc]
        panel_path = os.path.join(panel_dir, f'panel_{panel_count:02d}.png')
        save_image(panel, panel_path, mode='RGB')
        panel_count += 1

    print(f"Saved {panel_count} panels to '{panel_dir}'.")

# 👇 Hardcoded function call
segment_panels(
    image_path=r"C:\Users\derra\PycharmProjects\ComicToNarration\Data\Starting_page.png",
    output_dir=r"C:\Users\derra\PycharmProjects\ComicToNarration\Data"
)

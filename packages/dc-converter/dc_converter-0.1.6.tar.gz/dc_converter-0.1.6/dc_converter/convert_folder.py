import os
import shutil
from typing import List

from typing import Any, Dict, Tuple

import dc_converter
import numpy as np
import cv2
import matplotlib.pyplot as plt
from dc_converter.dc_converter import convert_file, read_raw_file, convert_depth_file


def convert_file_inplace(raw_file_name: str):
    # Remove 'raw' from filename:
    name_wo_extension = raw_file_name[0:-3]

    # Add target names:
    depth_file_name = name_wo_extension + 'tiff'
    infrared_file_name = name_wo_extension + 'png'

    if not os.path.exists(depth_file_name) and not os.path.exists(infrared_file_name):
        dc_converter.convert_file(raw_file_name, 0.015, 0.0)


def convert_depth_file_target(raw_file_name: str, target_file_name: str):
    convert_depth_file(raw_file_name, target_file_name)


def convert_to_folder(raw_file_name: str, target_folder: str):
    # Extract file name and remove 'raw':
    name_wo_extension = os.path.basename(raw_file_name)[0:-3]

    # Add target names:
    depth_file_name = os.path.join(target_folder, name_wo_extension + 'tiff')
    infrared_file_name = os.path.join(target_folder, name_wo_extension + 'png')

    if not os.path.exists(depth_file_name) and not os.path.exists(infrared_file_name):
        print(f'Converting {raw_file_name} to {depth_file_name} and {infrared_file_name}')
        convert_file(raw_file_name, depth_file_name, infrared_file_name, 0.015, 0.0)


def copy_converted_files(target_file: str, target_folder: str):
    # Get filename without extension:
    name_wo_extension = os.path.basename(target_file)[0:-3]
    inplace_folder = os.path.dirname(target_file)
    target_tiff = os.path.join(inplace_folder, name_wo_extension + 'tiff')
    target_png = os.path.join(inplace_folder, name_wo_extension + 'png')
    if not os.path.exists(target_tiff) or not os.path.exists(target_png):
        shutil.copyfile(os.path.join(target_folder, name_wo_extension + 'tiff'), target_tiff)
        shutil.copyfile(os.path.join(target_folder, name_wo_extension + 'png'), target_png)


def write_color_images(raw_file_name: str):
    depth, infrared, _, _, _ = read_raw_file(raw_file_name)

    depth_img = cv2.Mat(np.array(depth, np.uint16)).reshape((240, 320))
    depth_img = cv2.rotate(depth_img, cv2.ROTATE_90_CLOCKWISE)

    infrared_img = cv2.Mat(np.array(infrared, np.uint16)).reshape((240, 320))
    infrared_img = cv2.rotate(infrared_img, cv2.ROTATE_90_CLOCKWISE)

    # cv2.imwrite('test.png', infrared_img)

    _store_color_map(depth_img, 'depth_c.png', (100, 2500), {})
    _store_color_map(infrared_img, 'color.png', (100, 1000), {})

    _store_histogramm(depth_img.ravel(), 'hist.png')


def write_multi_view(raw_file_name: str, target_file_name: str):
    depth, infrared, t_int, t_ext, exposure = read_raw_file(raw_file_name)

    depth_img = cv2.Mat(np.array(depth, np.uint16)).reshape((240, 320))
    depth_img = cv2.rotate(depth_img, cv2.ROTATE_90_CLOCKWISE)

    infrared_img = cv2.Mat(np.array(infrared, np.uint16)).reshape((240, 320))
    infrared_img = cv2.rotate(infrared_img, cv2.ROTATE_90_CLOCKWISE)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 9),
                                        gridspec_kw={'width_ratios': [2, 2, 1]})

    ax1.imshow(infrared_img, cmap='viridis')
    ax1.axis('off')

    ax1.text(5, 30,
             f"t Sensor:     {t_int}°C\n"
             f"t LED:          {t_ext}°C\n"
             f"Exposure:  {exposure}",
             color="white", fontsize=14)

    ax2.imshow(depth_img, cmap='hot')
    (ax2.axis('off'))

    ax3.hist(depth_img.ravel(), bins=128, range=(0.0, 1500.0), fc='k', ec='k')

    fig.tight_layout()

    # Create folder when not existing:
    os.makedirs(os.path.dirname(target_file_name), exist_ok=True)

    plt.savefig(target_file_name, bbox_inches="tight",
                pad_inches=0.01, dpi=250)
    plt.close()


def _scan_files(path: str, extension: str) -> List[str]:
    """ Find all raw files in folder. """
    raw_files: List[str] = []

    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                raw_files.append(os.path.join(root, file))

    return raw_files


def _store_color_map(img, file_name: str, value_limits: Tuple[float, float], metadata: Dict[str, Any] = None):
    # Lazy load, not needed for writing only tiff:

    plt.clf()
    plt.imshow(img, clim=value_limits)
    plt.colorbar()
    plt.savefig(file_name, bbox_inches="tight",
                pad_inches=0.02, dpi=250)
    plt.close()


def _store_histogramm(img, file_name: str, metadata: Dict[str, Any] = None):
    plt.clf()
    plt.hist(img.ravel(), bins=128, range=(0.0, 1500.0), fc='k', ec='k')

    plt.savefig(file_name, bbox_inches="tight",
                pad_inches=0.02, dpi=250,
                metadata=metadata)
    plt.close()

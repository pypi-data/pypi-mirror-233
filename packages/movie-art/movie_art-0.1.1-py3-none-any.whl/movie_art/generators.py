'''
__main__.py
'''

import cv2
import numpy as np
import pathlib

from .constants import *    #pylint: disable=wildcard-import


def generate(input: pathlib.Path, output: pathlib.Path, width: int, height: int) -> int:
    '''
    generate()
    '''

    try:
        # get the video's properties
        video = cv2.VideoCapture(str(input))             # pylint: disable=no-member
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))  # pylint: disable=no-member
        frames_per_slit = int(frame_count / (width - 1))
        total_slits = int(frame_count / frames_per_slit)

        # create empty output image
        image_result = np.zeros((height, width, 3), dtype=np.uint8)
        image_result[:] = (0, 0, 0) # BGR (black)

        # iterate through each frame of the video
        for frame_index in range(0, frame_count, frames_per_slit):
            # print progress
            current_slit = int(frame_index / frames_per_slit)
            progress = f'Processing Slit: {current_slit}/{total_slits}, \
                         Frame: {frame_index}/{frame_count}'
            print(progress, end='\r')

            # read the frame
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_index) # pylint: disable=no-member
            _, frame = video.read()

            # get the average color
            frame_np = np.array(frame)
            total_pixels = frame_np.shape[0] * frame_np.shape[1]
            average_color = (
                np.sum(frame_np[:, :, 0]) / total_pixels, # blue
                np.sum(frame_np[:, :, 1]) / total_pixels, # green
                np.sum(frame_np[:, :, 2]) / total_pixels # red
            )

            # update the output image
            image_result[:, current_slit, :] = average_color

            # show preview windows
            if SHOW_PREVIEW:
                cv2.imshow(INPUT_PREVIEW_WINDOW_ID, frame)
                cv2.setWindowTitle(INPUT_PREVIEW_WINDOW_ID, progress)

                cv2.imshow(OUTPUT_PREVIEW_WINDOW_ID, image_result)
                cv2.setWindowTitle(OUTPUT_PREVIEW_WINDOW_ID, progress)
                cv2.waitKey()

        # save the output image
        cv2.imwrite(str(output), image_result)   # pylint: disable=no-member
        return 0

    except Exception as exception:  # pylint: disable=broad-exception-caught
        print(str(exception))
        return -1
    finally:
        video.release()
        cv2.destroyAllWindows() # pylint: disable=no-member

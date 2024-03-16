
from skimage.color import rgb2lab
import cv2
import numpy as np

class ImageCompletion():
    def __init__(self,image,mask,patch_size=5):
        self.image = image.astype('uint8')
        self.mask = mask.round().astype('uint8')
        self.patch_size = patch_size
        self.working_image = self.image
        self.working_mask = self.mask


    def _find_source_patch(self, target_pixel):
        target_patch = self._get_patch(target_pixel)
        height, width = self.working_image.shape[:2]
        patch_height, patch_width = self._patch_shape(target_patch)

        best_match = None
        best_match_difference = 0
        lab_image = rgb2lab(self.working_image)
        for y in range(height - patch_height + 1):
            for x in range(width - patch_width + 1):
                source_patch = [
                    [y, y + patch_height-1],
                    [x, x + patch_width-1]
                ]
                if self._patch_data(self.working_mask, source_patch)\
                    .sum() != 0:
                    continue

                difference = self._calc_patch_difference(
                    lab_image,
                    target_patch,
                    source_patch
                )

                if best_match is None or (difference < best_match_difference ):
                    best_match = source_patch
                    best_match_difference = difference
                    print(difference)
        return best_match_difference

    def _get_patch(self, point):
        half_patch_size = (self.patch_size-1)//2
        height, width = self.working_image.shape[:2]
        patch = [
            [
                max(0, point[0] - half_patch_size),
                min(point[0] + half_patch_size, height-1)
            ],
            [
                max(0, point[1] - half_patch_size),
                min(point[1] + half_patch_size, width-1)
            ]
        ]
        return patch

    def _patch_shape(self,patch):
        return (1+patch[0][1]-patch[0][0]), (1+patch[1][1]-patch[1][0])

    def _patch_data(self,source, patch):
        return source[
            patch[0][0]:patch[0][1]+1,
            patch[1][0]:patch[1][1]+1
        ]


    def _calc_patch_difference(self, image, target_patch, source_patch):
        mask = 1 -self._patch_data(self.working_mask, target_patch)
        rgb_mask = self._to_rgb(mask)
        target_data = self._patch_data(
            image,
            target_patch
        ) * rgb_mask
        source_data = self._patch_data(
            image,
            source_patch
        ) * rgb_mask
        squared_distance = ((target_data - source_data)**2).sum()
        euclidean_distance = np.sqrt(
            (target_patch[0][0] - source_patch[0][0])**2 +
            (target_patch[1][0] - source_patch[1][0])**2
        )  # tie-breaker factor
        return squared_distance+euclidean_distance

    def _to_rgb(self,image):
        height, width = image.shape
        return image.reshape(height, width, 1).repeat(3, axis=2)


if __name__ == "__main__":
    image_path="C:\\Users\\Siddharth\\OneDrive\\Desktop\\image1.jpg"
    mask_path="C:\\Users\\Siddharth\\OneDrive\\Desktop\\mask1.jpg"
    image = cv2.imread(image_path)
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    # print(mask.shape)
    output=ImageCompletion(
        image,
        mask,
        patch_size=9,
    )._find_source_patch(np.array([125,125],dtype=np.uint8))
    print(output)

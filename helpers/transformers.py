from torchvision import transforms
import collections
import torch
import numpy as np


def applyTransform(split, image, points, transform_name='basic', exp_dict=None):
    if transform_name == 'rgb_normalize':
        mean = [0.485, 0.456, 0.406]
        std = [0.229, 0.224, 0.225]
        # Transformation Sequence - 1st Function in each sub-list applies to image, 2nd to points
        transform = ComposeJoint(
            [
                [transforms.ToTensor(), None], #convert image to Tensor
                [transforms.Normalize(mean=mean, std=std), None], #normalize Image Tensor
                [None, ToLong()] # convert Points to Long Tensor (still binary)
            ])

        return transform([image, points])

class ComposeJoint(object):
    def __init__(self, transforms):
        self.transforms = transforms

    def __call__(self, x):
        for transform in self.transforms:
            x = self._iterate_transforms(transform, x)

        return x

    def _iterate_transforms(self, transforms, x):
        if isinstance(transforms, collections.Iterable):
            # split operations for image and points
            for i, transform in enumerate(transforms):
                x[i] = self._iterate_transforms(transform, x[i])
        else:
            if transforms is not None:
                x = transforms(x)

        return x

class ToLong(object):
    def __call__(self, x):
        return torch.LongTensor(np.asarray(x))
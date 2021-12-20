import cv2 as cv
import numpy as np

kernel = np.array([[256, 128, 64],
                   [32, 16, 8],
                   [4, 2, 1]])


def read_input(path):
    with open(path) as f:
        lines = f.read().splitlines()

    lookup = [1 if x == '#' else 0 for x in lines[0]]
    input_img_str = lines[2:]
    h, w = len(input_img_str), len(input_img_str[0])

    in_img = np.zeros((h, w), dtype=np.uint16)
    for i in range(h):
        for j in range(w):
            if input_img_str[i][j] == '#':
                in_img[i, j] = 1

    return lookup, in_img


def step(in_img, lookup, padding):
    # pad image
    padded = cv.copyMakeBorder(in_img, 2, 2, 2, 2, cv.BORDER_CONSTANT, value=padding)

    # Convolve image
    convolved = cv.filter2D(padded, cv.CV_16UC1, kernel, borderType=cv.BORDER_CONSTANT)
    convolved = convolved[1:-1, 1:-1]

    # Convolve padding
    conv_pad = cv.filter2D(np.ones((3, 3), dtype=np.uint16) * padding, cv.CV_16UC1, kernel, borderType=cv.BORDER_ISOLATED)
    new_padding = lookup[conv_pad[1][1]]

    # Use lookup to get output image
    out = np.array([[lookup[convolved[i, j]] for j in range(convolved.shape[1])] for i in range(convolved.shape[0])], dtype=np.uint16)

    return out, new_padding


# lookup, img = read_input('test.txt')
lookup, img = read_input('input.txt')
padding = 0

for i in range(50):
    img, padding = step(img, lookup, padding)

print(f"Padding val:{padding}")
print(f"Lit pixels: {np.sum(img)}")

import numpy as np

img = np.full((4,4), 250, dtype=np.uint8)

# print(img)
# print(img + np.uint8(10))

def brighten(img: np.ndarray, delta: int) -> np.ndarray:
    result = img.astype(np.int16) + delta
    result = np.clip(result, 0, 255)
    return result.astype(np.uint8)


if __name__ == '__main__':
    naive = img + np.uint8(10)
    assert np.all(naive == 4)  # 250+10=260, заворачивается по модулю 256

    bright = brighten(img, 10)
    assert np.all(bright == 255)  # 250+10=260, клипается к 255
    assert bright.dtype == np.uint8

    dark = brighten(img, -300)
    assert np.all(dark == 0)  # 250-300 < 0, клипается к 0
    assert dark.dtype == np.uint8

    mid = brighten(img, -10)
    assert np.all(mid == 240)  # 250-10=240, в границах, без клипа

    print('all tests passed')
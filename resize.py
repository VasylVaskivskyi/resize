import cv2 as cv
import tifffile as tif
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', type=str, help='path to image file')
parser.add_argument('-s', type=float, help='scale in fractions of 1. 1=original size, 0.5=half size')

args = parser.parse_args()

print('started')
path = args.i
scale = args.s
with tif.TiffFile(path) as TF:
    npages = len(TF.pages)
    meta = TF.ome_metadata



with tif.TiffWriter(path.replace('.tif','_resized.tif')) as TW:
    for i in range(0, npages):
        print('page' + str(i + 1) + '/' + str(npages))
        img = tif.imread(path, key=i)

        img_shape = img.shape
        print('original size', str(img_shape))
        new_shape = (int(round(img_shape[1] * scale)), int(round(img_shape[0] * scale)) )
        resized = cv.resize(img, new_shape, None, interpolation=cv.INTER_CUBIC)
        print('new size', str(new_shape))
        if meta is not None:
            meta = meta.replace('SizeX="' + str(img_shape[1]) + '"', 'SizeX="' + str(new_shape[1]) + '"')
            meta = meta.replace('SizeY="' + str(img_shape[0]) + '"', 'SizeY="' + str(new_shape[0]) + '"')
        TW.save(resized, photometric='minisblack', description=meta)

print('finished')

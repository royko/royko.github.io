import glob
from PIL import Image

### include / at end
dirname_input = "/Users/royko/EAS/2024-02-15-sunset1500-1840/"

### does not check inputs
def filename_from_time_direction(time, direction):
    ### could do some checks here
    filenameglob = "EAScam-%s.2024-02-15.%s*.jpg" % (direction, time)
#    print (dirname_input + filenameglob)
    filenames = glob.glob(dirname_input + filenameglob)
    ### should check if we didn't get any
    return filenames[0]

time_start = 1700
time_end = 1905

### assumes that all images are same size

# make this the leftmost image, to make downstream work
image = Image.open(filename_from_time_direction(time_start, 'w'))
image_width_in, image_height = image.size

image_width = image_width_in * 4

print(image_width)
print(image_height)

### the following magic is a HACK
images_count = time_end - time_start + 1 - ((int(time_end/100) - int(time_start/100)) * 40)

print(images_count)

# you might want to make the slices narrower by subtracting a fudge factor
slice_trim = 2
slice_width = int(image_width / images_count) - slice_trim

margin_left = int((image_width - (slice_width * images_count))/2)

print(margin_left)
print("%s left margin, then %s x %s slices, leaving %s right margin" %
      (margin_left, images_count, slice_width,
       image_width - (images_count * slice_width) - margin_left))


# output canvas
image_out = Image.new('RGB', (image_width, image_height))

#paste the first image at the left edge of the canvas
image_out.paste(image)
#paste the last image at the right edge of the canvas
image = Image.open(filename_from_time_direction(time_end, 'e'))
image_out.paste(image,(image_width - image.width, 0))

#image_out.save('debug.png')

count = 0
for t in range(time_start, time_end + 1, 1):
    if ((t % 100) > 59):
        continue
#    print (t)
    position = margin_left + (count * slice_width)
#    print("image %s at column %s for %s pixels" % (count, position, slice_width))
    count += 1
    
    im1 = Image.open(filename_from_time_direction(t, 'w'))
    im2 = Image.open(filename_from_time_direction(t, 'nw'))
    im3 = Image.open(filename_from_time_direction(t, 'ne'))
    im4 = Image.open(filename_from_time_direction(t, 'e'))
    image = Image.new('RGB', (image_width, image_height))
    image.paste(im1, (0, 0))
    image.paste(im2, (image_width_in, 0))
    image.paste(im3, (image_width_in * 2, 0))
    image.paste(im4, (image_width_in * 3, 0))
    slice = image.crop((position, 0, position + slice_width, image_height))
    image_out.paste(slice, (position, 0))

image_out.save('out.png')



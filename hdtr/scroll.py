import glob
from PIL import Image

# the following tolerates the error
# OSError: image file is truncated (130 bytes not processed)
# which is OK if the truncation is at the bottom
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

### include / at end
### CHANGE ME
dirname_input = "/Users/royko/EAS/2024-02-18/"

### does not check inputs
def filename_from_time_direction(time, direction):
    time_str = f"{time:04d}"
    ### CHANGE ME
    filenameglob = "EAScam-%s.2024-02-18.%s*.jpg" % (direction, time_str)
#    print (dirname_input + filenameglob)
    filenames = glob.glob(dirname_input + filenameglob)
    ### should check if we didn't get any
    if (len(filenames) < 1):
        print ("glob %s%s produces no files" % (dirname_input, filenameglob))
        print ("trying to substitute time %s..." % (time - 1))
        if (time == 0):
            print ("Nope.  You'd better solve this.")
            exit()
        return filename_from_time_direction(time - 1, direction)
    return filenames[0]

# if you get an error message like
# glob /Users/royko/EAS/2024-01-24/EAScam-e.2024-01-24.0013*.jpg produces no files
# do
# (hdtr) royko@TMWY9LH4P3 hdtr % cp /Users/royko/EAS/2024-01-24/EAScam-e.2024-01-24.001226.jpg /Users/royko/EAS/2024-01-24/EAScam-e.2024-01-24.001399.jpg


### CHANGE ME
time_start = 450
time_end = 1748
#time_end = 1804
#time_end = 1817
#time_end = 1824

images_count = time_end - time_start + 1 - ((int(time_end/100) - int(time_start/100)) * 40)

print("%s using %s images from %s to %s" % (dirname_input, images_count, time_start, time_end))

### assumes that all images are same size

image = Image.open(filename_from_time_direction(time_start, 'w'))
image_width_in, image_height_in = image.size

### CHANGE ME
slice_height = 1

#trim 24 pixels from the top to get rid of the timestamp
top_crap_height = 24
image_width_out = image_width_in * 4
image_height_out = image_height_in + ((images_count - 1) * slice_height) - top_crap_height
slice_width = image_width_out

print("output image %s x %s (%s pixel slices)" % (image_width_out, image_height_out, slice_height))


# output canvas
image_out = Image.new('RGB', (image_width_out, image_height_out))

count = 0
for t in range(time_start, time_end + 1, 1):
    if ((t % 100) > 59):
        continue
    #print (f"{t:04d}")
    #can also str(t).zfill(4)
    top_margin = (count * slice_height)
    count += 1
    
    im1 = Image.open(filename_from_time_direction(t, 'w'))
    im2 = Image.open(filename_from_time_direction(t, 'nw'))
    im3 = Image.open(filename_from_time_direction(t, 'ne'))
    im4 = Image.open(filename_from_time_direction(t, 'e'))
    image = Image.new('RGB', (image_width_out, image_height_in))
    image.paste(im1, (0, 0))
    image.paste(im2, (image_width_in, 0))
    image.paste(im3, (image_width_in * 2, 0))
    image.paste(im4, (image_width_in * 3, 0))
    slice = image.crop((0, top_crap_height, image_width_out, image_height_in))
    image_out.paste(slice, (0, top_margin))

# image is now the last image from the loop
#image_out.paste(image, (0, top_margin))
image_out.save('out.png')



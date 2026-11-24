import subprocess

#Exercise 2: Color space conversion
class ColorTranslator:
    def rgb_to_yuv(r, g, b):
        # Coeficients BT.601: Kr = 0.299, Kg = 0.587, Kb = 0.114
        y = 0.299 * r + 0.587 * g + 0.114 * b
        u = -0.14713 * r - 0.28886 * g + 0.436 * b
        v = 0.615 * r - 0.51499 * g - 0.10001 * b
        return y, u, v
    
    def yuv_to_rgb(y, u, v):
        # Inverse matrix of the RGB to YUV transformation
        r = y + 1.13983 * v
        g = y - 0.39465 * u - 0.58060 * v
        b = y + 2.03211 * u
        return r, g, b

#https://blog.csdn.net/qq_34952376/article/details/136813279
#https://en.wikipedia.org/wiki/YCbCr#ITU-R_BT.601_conversion

y,u,v = ColorTranslator.rgb_to_yuv(25, 255, 3)
r,g,b = ColorTranslator.yuv_to_rgb(y, u, v)

print(f"RGB: ({r:.4f}, {g:.4f}, {b:.4f})")
# Result: RGB: (24.9996, 255.0003, 3.0016)
# As shown above, the round-trip conversion introduces a
# minor rounding error. This is due to floating-point precision 
# and the truncated coefficients in the transformation matrices.

#Exercise 3: The chroma lie
#We have executed the following commands in our terminal:
# ffmpeg -i image.png -pix_fmt yuv444p out444.jpg
# ffmpeg -i image2.png -pix_fmt yuv422p out4222.jpg
# ffmpeg -i image.png -pix_fmt yuv420p out420.jpg
# ffmpeg -i image.png -pix_fmt yuv411p out411.jpg

# We can see that the 4:4:4 format yields the best result, 
# as it preserves the chromatic aberration present in the original image, 
# whereas in the other formats, these details progressively disappear.
# Although some compression artifacts appear,
# the overall visual difference is barely noticeable to the human eye.

#We have executed the following commands in our terminal to extract the Y, U and V channels from the image:
#ffmpeg -i image.png -vf "format=yuv444p,extractplanes=y" Y.png
#ffmpeg -i image.png -vf "format=yuv444p,extractplanes=u" U.png
#ffmpeg -i image.png -vf "format=yuv444p,extractplanes=v" V.png

#Blurred Chroma (U and V channels):
#ffmpeg -i U.png -vf gblur=sigma=20 U_blur.png
#ffmpeg -i V.png -vf gblur=sigma=20 V_blur.png
#ffmpeg -i Y.png -i U_blur.png -i V_blur.png -filter_complex "[0][1][2]mergeplanes=0x001020:yuv444p" blur_chroma.png

#Blurred Luma (Y channel):
#ffmpeg -i Y.png -vf gblur=sigma=20 Y_blur.png
#ffmpeg -i Y_blur.png -i U.png -i V.png -filter_complex "[0][1][2]mergeplanes=0x001020:yuv444p" blur_luma.png

#https://ffmpeg.org/documentation.html

#We noticed more the blur in the luma channel than in the chroma channels.

# JPEG and video codecs apply chroma subsampling (like 4:2:0) because the human visual system
# is more sensitive to luminance (brightness) than to chrominance (color).
# By storing color channels at a lower spatial resolution, codecs reduce file size 
# and bandwidth with almost no perceptible loss in visual quality.

#All the results of the exercise 3 can be found in the "Exercise3_sources" folder.


#Exercise 4:
valid_factors = [2, 4, 8]
valid_algorithms = ["bilinear", "bicubic", "lanczos", "neighbor"]

def image_resize(resizing_factor, img, algorithm=""):

    if ((resizing_factor in valid_factors) and algorithm == ""):
        scale = f"scale=iw/{resizing_factor}:ih/{resizing_factor}"
        output = f"output_4/resized_{resizing_factor}.jpg"
        subprocess.run(["ffmpeg", "-i", img, "-update", "1", "-vf", scale, output], check=True)
        
    elif ((resizing_factor in valid_factors) and (algorithm in valid_algorithms)):
        scale = f"scale=iw/{resizing_factor}:ih/{resizing_factor}"
        output = f"output_4/resized_{resizing_factor}_{algorithm}.jpg"
        subprocess.run(["ffmpeg", "-i", img, "-update", "1", "-vf", scale, "-sws_flags", algorithm, output], check=True)
        
    else:
        print("\nERROR: Invalid resizing factor.\n")


image1 = "input/sonice-adventure-pose-1299062768.jpg"

image_resize(resizing_factor=2, algorithm="lanczos", img=image1)
image_resize(resizing_factor=4, algorithm="lanczos", img=image1)
image_resize(resizing_factor=8, algorithm="lanczos", img=image1)
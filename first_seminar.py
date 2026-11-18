
#Exercise 2: Color space conversion
class ColorTranslator:
    def rgb_to_yuv(r, g, b):
        # Coeficients BT.601: Kr = 0.299, Kg = 0.587, Kb = 0.114
        y = 0.299 * r + 0.587 * g + 0.114 * b
        u = -0.14713 * r - 0.28886 * g + 0.436 * b
        v = 0.615 * r - 0.51499 * g - 0.10001 * b
        return y, u, v
    
    def yuv_to_rgb(y, u, v):
        # Matriu inversa de la transformació RGB a YUV
        r = y + 1.13983 * v
        g = y - 0.39465 * u - 0.58060 * v
        b = y + 2.03211 * u
        return r, g, b

#https://blog.csdn.net/qq_34952376/article/details/136813279
#https://en.wikipedia.org/wiki/YCbCr#ITU-R_BT.601_conversion

#Exercise 3: The chroma lie
#We have executed the following commands in our terminal:
# ffmpeg -i image.png -pix_fmt yuv444p out444.jpg
# ffmpeg -i image.png -pix_fmt yuv422p out422.jpg
# ffmpeg -i image.png -pix_fmt yuv420p out420.jpg
# ffmpeg -i image.png -pix_fmt yuv411p out411.jpg

#
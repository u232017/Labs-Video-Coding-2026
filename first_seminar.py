import subprocess


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

# - Which scaling algorithm does FFmpeg use by default?
# ANSWER: 

# Exercise 5:

def zigzag (matrix):
    output = []
    
    i,j = 0,0
    for i in range(8):
        for j in range(8):
            if ((i % 2) == 0):
                output.append(matrix[i][j])
            else:
                new_j = abs(j - 7)
                output.append(matrix[i][new_j])
    return output

def inverse_zigzag (list):
    output_matrix = []

    for i in range(8):
        row = []
        for j in range(8):
            if (i % 2 == 0):
                row.append(list[i * 8 + j])
            else:
                row.append(list[i * 8 + (7 - j)])

        output_matrix.append(row)

    return output_matrix

mat = [[1,2,3,4,5,6,7,8], [9,10,11,12,13,14,15,16], [17,18,19,20,21,22,23,24], [25,26,27,28,29,30,31,32], 
       [33,34,35,36,37,38,39,40], [41,42,43,44,45,46,47,48], [49,50,51,52,53,54,55,56], [57,58,59,60,61,62,63,64]]

output_list = zigzag(mat)
print(output_list)

output_mat = inverse_zigzag(output_list)
print(output_mat)

# - Why this order? One line is enough
# ANSWER: 
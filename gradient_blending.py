'''image blending for single-channel images
'''
import numpy as np
import cv2 as cv
from numpy.linalg import inv

def get_image_mask(source_img):
    '''create the mask
    in the contour: white region with pixel intensity 255
    outside of the contour: black region with pixel intensity 0
    '''
    mask = np.zeros(source_img.shape)
    mask[source_img!=255] = 255
    return mask

def get_index(mask, height, width, offset_x, offset_y):
    indexes = np.zeros((height, width))
    mask_height, mask_width = mask.shape
    p = 1
    # we should optimize this part of code
    for i in range(offset_y, mask_height+offset_y):
        for j in range(offset_x, mask_width+offset_x):
            if mask[i-offset_y][j-offset_x] != 0:
                indexes[i][j] = p
                p += 1
    return indexes

def pad_with(vector, pad_width, iaxis, kwargs):
    pad_value = kwargs.get('padder', 10)
    vector[:pad_width[0]] = pad_value
    vector[-pad_width[1]:] = pad_value

def get_coefficient_matrix(indexes):
    '''pass testing, check if we can optimize
    A * f - c (target) = b (source) 
    laplacian gradient of target_image = laplacian gradient of source_image
    '''
    indexes_pad = np.pad(indexes, 1, pad_with, padder=0).astype('int32')  
    num = sum(sum(indexes != 0))
    coeff_A = 4 * np.eye(num)
    
    for i in range(1, num+1):
        m, n = np.where(indexes_pad == i)[0][0], np.where(indexes_pad == i)[1][0]


        up = indexes_pad[m-1][n]
        if up != 0:
            coeff_A[i-1][up-1] = -1

        down = indexes_pad[m+1][n]
        if down != 0:
            coeff_A[i-1][down-1] = -1

        left = indexes_pad[m][n-1]
        if left != 0:
            coeff_A[i-1][left-1] = -1

        right = indexes_pad[m][n+1]
        if right != 0:
            coeff_A[i-1][right-1] = -1

    return coeff_A

def get_vector(indexes, source_img, target_img, offset_x, offset_y):
    num = sum(sum(indexes != 0))
    vector_b = np.zeros((num,1))
    source_img = np.pad(source_img, 1, pad_with, padder=0)
    target_img = np.pad(target_img, 1, pad_with, padder=0)
    indexes_pad = np.pad(indexes, 1, pad_with, padder=0)    
    
    for i in range(1,num+1):
        up, down, left, right = 0, 0, 0, 0
        m, n = np.where(indexes_pad == i)[0][0], np.where(indexes_pad == i)[1][0] 
        if indexes_pad[m-1][n] == 0:
            up = target_img[m-1][n]
        if indexes_pad[m+1][n] == 0:
            down = target_img[m+1][n]
        if indexes_pad[m][n-1] == 0:
            left = target_img[m][n-1]
        if indexes_pad[m][n+1] == 0:
            right = target_img[m][n+1]
        m1 = m - offset_y
        n1 = n - offset_x
        vector_b[i-1][0] = 4 * source_img[m1][n1] - source_img[m1-1][n1] - source_img[m1+1][n1] - \
            source_img[m1][n1-1] - source_img[m1][n1+1] + up + down + left + right 

    return vector_b


def reconstruct_img(indexes, x, target_img):
    num = sum(sum(indexes != 0))
    for i in range(1, num+1):
        m, n = np.where(indexes == i)[0][0], np.where(indexes == i)[1][0] 
        target_img[m][n] = x[i-1][0]
    return target_img

def seamless_clone_poisson(source_img, target_img, mask, offset_x, offset_y):
    height, width = target_img.shape
    indexes = get_index(mask, height, width, offset_x, offset_y) # pass
    # get vector b
    vector_b = get_vector(indexes, source_img, target_img, offset_x, offset_y) # pass
    # get matrix A
    coeff_A = get_coefficient_matrix(indexes) # pass
    # get x
    x = np.matmul(inv(coeff_A), vector_b)
    #print("x is {}".format(x))
    #x = vector_b / coeff_A
    # get the result image
    return reconstruct_img(indexes, x, target_img)

# *** debug the code ***
source_img = cv.imread("./picture/src_img_2.png")
target_img = cv.imread("./picture/target_img.png")
source_img = cv.cvtColor(source_img, cv.COLOR_BGR2GRAY)
target_img = cv.cvtColor(target_img, cv.COLOR_BGR2GRAY)
mask = get_image_mask(source_img).astype('int32')
value = 200
source_img = source_img - value * np.ones(source_img.shape)
source_img[source_img==(255-value)]=255
source_img = np.clip(source_img, a_min=0, a_max=255) 
# **********************

# *** small test example ***
# source_img = np.array([[1,2,3],
#                        [5,6,7],
#                        [1,6,9]])
# print("the source image pre is \n {}".format(source_img))                       
# target_img = np.array([[3,3,3,3,3,3],
#                        [4,4,4,4,4,4],
#                        [5,5,5,5,5,5],
#                        [6,6,6,6,6,6],
#                        [3,3,3,3,3,3],
#                        [2,2,2,2,2,2]])
# mask = np.array([[0,0,255],
#                  [0,255,255],
#                  [255,0,0]])
# source_img[mask==255] -= 3
# print("the source image post is \n {}".format(source_img))   
# ***************************

offset_x = 1000
offset_y = 1000
result_img = seamless_clone_poisson(source_img, target_img, mask, offset_x, offset_y)
#print("result image is {}".format(result_img))
cv.imwrite("./picture/output_img_12.png", result_img)



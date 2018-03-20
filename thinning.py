# -*- coding: utf-8 -*-
"""
===========================
@Original Author  : Linbo<linbo.me>
@Updated Author  : Sunny.Xia
===========================
"""
#import matplotlib
#import matplotlib.pyplot as plt
#import skimage.io as io
import scipy.misc
import numpy as np
from PIL import Image,ImageDraw,ImageOps
from skimage.filters import threshold_otsu
from filepath import read_allfiles_underDir

def neighbours(x,y,image):
    "Return 8-neighbours of image point P1(x,y), in a clockwise order"
    img = image
    x_1, y_1, x1, y1 = x-1, y-1, x+1, y+1
    return [ img[x_1][y], img[x_1][y1], img[x][y1], img[x1][y1],     # P2,P3,P4,P5
                img[x1][y], img[x1][y_1], img[x][y_1], img[x_1][y_1] ]    # P6,P7,P8,P9

def transitions(neighbours):
    "No. of 0,1 patterns (transitions from 0 to 1) in the ordered sequence"
    n = neighbours + neighbours[0:1]      # P2, P3, ... , P8, P9, P2
    return sum( (n1, n2) == (0, 1) for n1, n2 in zip(n, n[1:]) )  # (P2,P3), (P3,P4), ... , (P8,P9), (P9,P2)

def zhangSuen(image):
    "the Zhang-Suen Thinning Algorithm"
    Image_Thinned = image.copy()  # deepcopy to protect the original image
    changing1 = changing2 = 1        #  the points to be removed (set as 0)
    while changing1 or changing2:   #  iterates until no further changes occur in the image
        # Step 1
        changing1 = []
        rows, columns = Image_Thinned.shape               # x for rows, y for columns
        for x in range(1, rows - 1):                     # No. of  rows
            for y in range(1, columns - 1):            # No. of columns
                P2,P3,P4,P5,P6,P7,P8,P9 = n = neighbours(x, y, Image_Thinned)
                if (Image_Thinned[x][y] == 1     and    # Condition 0: Point P1 in the object regions 
                    2 <= sum(n) <= 6   and    # Condition 1: 2<= N(P1) <= 6
                    transitions(n) == 1 and    # Condition 2: S(P1)=1  
                    P2 * P4 * P6 == 0  and    # Condition 3   
                    P4 * P6 * P8 == 0):         # Condition 4
                    changing1.append((x,y))
        for x, y in changing1: 
            Image_Thinned[x][y] = 0
        # Step 2
        changing2 = []
        for x in range(1, rows - 1):
            for y in range(1, columns - 1):
                P2,P3,P4,P5,P6,P7,P8,P9 = n = neighbours(x, y, Image_Thinned)
                if (Image_Thinned[x][y] == 1   and        # Condition 0
                    2 <= sum(n) <= 6  and       # Condition 1
                    transitions(n) == 1 and      # Condition 2
                    P2 * P4 * P8 == 0 and       # Condition 3
                    P2 * P6 * P8 == 0):            # Condition 4
                    changing2.append((x,y))    
        for x, y in changing2: 
            Image_Thinned[x][y] = 0
    return Image_Thinned
 
def skeleton_extraction(source,target1,target2):
	#filename='test8'
	#source='./data/%s.png'%filename
	#source=filepath
	'''
	icon下载的png，透明部分的RGB为0，所以转化成灰度图L的时候对应的灰度值也为0了
	'''
	"Convert png images to grey images"
	img=scipy.misc.imread(source,mode='RGBA')
	# 透明度为0的，RGB都设置成255，即设置为白色，这样再转化成灰度图的时候灰度值才不会为0，而是255  
	for i in range(0,3):
		img[:,:,i]=np.where(img[:,:,3]==0,255,img[:,:,i])

	img2=scipy.misc.toimage(img) # 转化成PIL
	Img_Original=scipy.misc.fromimage(img2,mode='L') # 再转化成灰度图L的矩阵形式
	#print Img_Original

	#scipy.misc.imsave
	#Img_Original =  io.imread( './data/%s.bmp'%filename)      # Gray image, rgb images need pre-conversion
	#print Img_Original
	#print 'img_original',Img_Original
	"Convert gray images to binary images using Otsu's method"
	Otsu_Threshold = threshold_otsu(Img_Original)   # 如果图中要么就是0，要么就是255的话，算出来的阈值就是0，此时就要手动设置成阈值127
	print 'threshold',Otsu_Threshold 
	if Otsu_Threshold==0:
		Otsu_Threshold=127
	 
	#Otsu_Threshold=127
	BW_Original = Img_Original < Otsu_Threshold    # must set object region as 1, background region as 0 ! 要求区域是黑色的，对应为1；背景是白色的，对应为0
	#print BW_Original
	BW_Skeleton = zhangSuen(BW_Original)   # 其中线条的部分对应True，背景部分对应false
	# 因为在binary image中，0是white，1是black，所以这里xor
	scipy.misc.imsave(target1,BW_Original^1)
	scipy.misc.imsave(target2,BW_Skeleton^1)
	#print 'BW_Skeleton.shape',BW_Skeleton.shape
	#scipy.misc.imsave(BW_Skeleton,'results/%s_target.jpg')%filename
	#BW_Skeleton.save('results/%s_target.jpg')    np.array
	# BW_Skeleton = BW_Original
	'''
	"Display the results"
	fig, ax = plt.subplots(1, 2)
	ax1, ax2 = ax.ravel()
	ax1.imshow(BW_Original, cmap=plt.cm.gray)
	ax1.set_title('Original binary image')
	ax1.axis('off')
	ax2.imshow(BW_Skeleton, cmap=plt.cm.gray)
	ax2.set_title('Skeleton of the image')
	ax2.axis('off')
	plt.show()
	plt.savefig('results/%s_res.jpg'%filename)
	'''

if __name__ == "__main__":
	input_path=u'D:\\研\\icon\\crawler\\iconsdb-64'
	"looking for all .png files under the input_path"
	image_files=read_allfiles_underDir(input_path,'.png')
	cnt=0
	for source in image_files:
		"the name of the image file"
		name=source.split('\\')[-1].split('.')[0]  
		cnt+=1
		print cnt,name
		target1='output/%s_src.bmp'%name  # the binary image of the source
		target2='output/%s_res.bmp'%name  # the skeletonization result
		skeleton_extraction(source,target1,target2)
# -*- coding: utf-8 -*-   
import os  
      
def read_allfiles_underDir(file_dir,suffix='.png'):   
    L=[]   
    pathDir=os.listdir(file_dir)
    for file in pathDir:
    	if os.path.splitext(file)[1] == suffix:  
        	L.append(os.path.join(file_dir, file))  
    return L  
if __name__ == "__main__":
	print file_name(u'D:\\研\\生成式设计探索\\thinning\\Skeletonization-by-Zhang-Suen-Thinning-Algorithm-master\\input\\')
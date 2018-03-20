

##Skeletonization by thinning algorithm

The original code is from [Skeletonization-by-Zhang-Suen-Thinning-Algorithm](https://github.com/linbojin/Skeletonization-by-Zhang-Suen-Thinning-Algorithm).

However, it must read .bmp(grey-image) as input. And the result is shown by plt.show().

So I make some adjustment, the program can read all .png files under the given directory and extract their skeletons just for once.

Therefore, you don't need to convert RGBA to L before executing the code. And the results will be saved under the './output’ path.



### input

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
All you have to do is just to change the 'input_path' to your input directory.

### Dependencies

- python2.7
- numpy
- PIL
- skimage
- scipy

### Results

![](https://github.com/ruozhichen/Skeletonization-by-thinning-algorithm/blob/master/show.jpg)
import numpy as np
import matplotlib.pyplot as plt
import os
import skimage.color as color
import scipy.ndimage.interpolation as sni
import scipy.misc
import caffe

#%matplotlib inline
#plt.rcParams['figure.figsize'] = (12, 6)
#caffe.set_mode_cpu();
gpu_id = 0
caffe.set_mode_gpu()
caffe.set_device(gpu_id)

# Select desired model
net = caffe.Net('../models/colorization_deploy_v2.prototxt', '../models/colorization_release_v2.caffemodel', caffe.TEST)
# net = caffe.Net('../models/colorization_deploy_v2.prototxt', '../models/colorization_release_v2_norebal.caffemodel', caffe.TEST)
# net = caffe.Net('../models/colorization_deploy_v1.prototxt', '../models/colorization_release_v1.caffemodel', caffe.TEST)
# If you are training your own network, you may replace the *.caffemodel path with your trained network.

(H_in,W_in) = net.blobs['data_l'].data.shape[2:] # get input shape
(H_out,W_out) = net.blobs['class8_ab'].data.shape[2:] # get output shape

print 'Input dimensions: (%i,%i)'%(H_in,W_in)
print 'Output dimensions: (%i,%i)'%(H_out,W_out)

pts_in_hull = np.load('../resources/pts_in_hull.npy') # load cluster centers
net.params['class8_ab'][0].data[:,:,0,0] = pts_in_hull.transpose((1,0)) # populate cluster centers as 1x1 convolution kernel
print 'Annealed-Mean Parameters populated'

# load the original image
img_rgb = caffe.io.load_image('/var/www/colorization/image_input/636073199499635923-1927055912_Adolf_Hitler_cropped_restored.jpg')

img_lab = color.rgb2lab(img_rgb) # convert image to lab color space
img_l = img_lab[:,:,0] # pull out L channel
(H_orig,W_orig) = img_rgb.shape[:2] # original image size

# create grayscale version of image (just for displaying)
img_lab_bw = img_lab.copy()
img_lab_bw[:,:,1:] = 0
img_rgb_bw = color.lab2rgb(img_lab_bw)
scipy.misc.imsave('./imgs/bewbs_bw.jpg',img_rgb_bw);

# resize image to network input size
img_rs = caffe.io.resize_image(img_rgb,(H_in,W_in)) # resize image to network input size
img_lab_rs = color.rgb2lab(img_rs)
img_l_rs = img_lab_rs[:,:,0]

# show original image, along with grayscale input to the network
img_pad = np.ones((H_orig,W_orig/10,3))
#plt.imshow(np.hstack((img_rgb, img_pad, img_rgb_bw)))
#plt.title('(Left) Loaded image   /   (Right) Grayscale input to network')
#plt.axis('off');

net.blobs['data_l'].data[0,0,:,:] = img_l_rs-50 # subtract 50 for mean-centering
net.forward() # run network

ab_dec = net.blobs['class8_ab'].data[0,:,:,:].transpose((1,2,0)) # this is our result
ab_dec_us = sni.zoom(ab_dec,(1.*H_orig/H_out,1.*W_orig/W_out,1)) # upsample to match size of original image L
img_lab_out = np.concatenate((img_l[:,:,np.newaxis],ab_dec_us),axis=2) # concatenate with original image L
img_rgb_out = np.clip(color.lab2rgb(img_lab_out),0,1) # convert back to rgb

#plt.imshow(img_rgb_out);
scipy.misc.imsave('./imgs/bewbs.jpg',img_rgb_out);
#plt.axis('off');


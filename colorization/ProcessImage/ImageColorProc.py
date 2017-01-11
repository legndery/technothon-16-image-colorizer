import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import os
import skimage.color as color
import scipy.ndimage.interpolation as sni
import scipy.misc
import caffe


#caffe.set_mode_cpu();
gpu_id = 0
caffe.set_mode_gpu()
caffe.set_device(gpu_id)

# Select desired model
net = caffe.Net('/var/www/colorization/models/colorization_deploy_v2.prototxt', '/var/www/colorization/models/colorization_release_v2.caffemodel', caffe.TEST)

(H_in,W_in) = net.blobs['data_l'].data.shape[2:] # get input shape
(H_out,W_out) = net.blobs['class8_ab'].data.shape[2:] # get output shape
	
print 'Input dimensions: (%i,%i)'%(H_in,W_in)
print 'Output dimensions: (%i,%i)'%(H_out,W_out)
	
pts_in_hull = np.load('/var/www/colorization/resources/pts_in_hull.npy') # load cluster centers
net.params['class8_ab'][0].data[:,:,0,0] = pts_in_hull.transpose((1,0)) # populate cluster centers as 1x1 convolution kernel
print 'Annealed-Mean Parameters populated'



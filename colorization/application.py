#import matplotlib
#matplotlib.use('Agg')
#import numpy as np
#import matplotlib.pyplot as plt
#import os
#import skimage.color as color
#import scipy.ndimage.interpolation as sni
#import scipy.misc
#import caffe


from flask import Flask
from web_controller.hello_world import hello
#from ProcessImage.ImageColorProc import *
from web_controller.upload_controller import *

app = Flask(__name__)

####CONFIG################

UPLOAD_FOLDER = '/var/www/colorization/image_input';
OUTPUT_FOLDER = '/var/www/colorization/image_output';

##########################
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER;
#########################

app.register_blueprint(hello)
app.register_blueprint(upload_controller)

if __name__ == '__main__':
	app.run(debug=True)

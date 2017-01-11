from flask import url_for,current_app, jsonify,Blueprint,render_template, request,send_from_directory
from werkzeug.utils import secure_filename
import sys,os, urllib, urllib2, urlparse
sys.path.insert(0, os.path.abspath('..'))
from ProcessImage.ImageColorProc import *
#import caffe
#import matplotlib
#matplotlib.use('Agg')
#import numpy as np
#import matplotlib.pyplot as plt
#import os
#import skimage.color as color
#import scipy.ndimage.interpolation as sni
#import scipy.misc

#global caffe
#global scipy.misc
#global color



ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg'])


upload_controller = Blueprint('upload_blueprint',__name__)

app = current_app


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@upload_controller.route('/uploads_bw/<filename>')
def uploaded_file_bw(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'],
                              "bw_proc_"+ filename)
@upload_controller.route('/uploads_color/<filename>')
def uploaded_file_color(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'],
                              "color_proc_"+ filename)
@upload_controller.route('/uploadLink', methods=['GET','POST'])
def uploadImageLink():
	if request.method== 'POST':
		#i love you <3
		returnJson = {'success':0,"status":"","message":"","result":""};
		link = request.form['url-link'];
		filename=urlparse.urlsplit(link).path.split('/')[-1]
		print filename;
		if filename and allowed_file(str(filename)):
			filename = secure_filename(filename);
			fullfilename = os.path.join(app.config['UPLOAD_FOLDER'], filename);
			print fullfilename
			f = urllib2.urlopen(link)
			data = f.read()
			with open(fullfilename, "wb") as code:
    				code.write(data)
			returnJson['success'] = 1;
                        returnJson["status"]="success";
                        returnJson["message"]="File uploaded Successfully";
                        returnJson["result"]={"bw":url_for('upload_blueprint.uploaded_file_bw',filename=filename), "color":url_for('upload_blueprint.uploaded_file_color',filename=filename)};
			global H_in
                        global W_in
                        #returnJson["Height"] = H_in;
                        #returnJson["Width"] = W_in;
			print filename
                        #process image
                        process_image(app.config['UPLOAD_FOLDER'],filename,returnJson)
                        #process image end
                        return jsonify(**returnJson)
		else :
			returnJson["status"]="failed";
                        returnJson["message"]="No file or file extension not allowed";
                        return jsonify(**returnJson)
	else:
		return '''
		<!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post>
      <p><input type=text name="url-link">
         <input type=submit value=submit>
    </form>'''		
		
@upload_controller.route('/upload',methods=['GET','POST'])
def uploadImage():
	if request.method == 'POST':
		returnJson = {'success':0,"status":"","message":"","result":""};
		if 'file' not in request.files:
			returnJson["status"]="failed";
			returnJson["message"]="No file to upload";
			return jsonify(**returnJson)
		fp = request.files['file']
		if fp.filename == '' :
			returnJson["status"]="failed";
                	returnJson["message"]="No file to upload";
			return jsonify(**returnJson)
		
		if fp and allowed_file(fp.filename):
			filename = secure_filename(fp.filename)
			fp.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			returnJson['success'] = 1;
			returnJson["status"]="success";
			returnJson["message"]="File uploaded Successfully";
			returnJson["result"]={"bw":url_for('upload_blueprint.uploaded_file_bw',filename=filename), "color":url_for('upload_blueprint.uploaded_file_color',filename=filename)};
			global H_in
			global W_in			
			#returnJson["Height"] = H_in;
			#returnJson["Width"] = W_in;
			
			#process image
			process_image(app.config['UPLOAD_FOLDER'],filename,returnJson)
			#process image end
			return jsonify(**returnJson)
	else:
		return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

def process_image(udir, filename, returnJson=None):
	# load the original image
	img_rgb = caffe.io.load_image(os.path.join(udir,filename))

	img_lab = color.rgb2lab(img_rgb) # convert image to lab color space
	img_l = img_lab[:,:,0] # pull out L channel
	(H_orig,W_orig) = img_rgb.shape[:2] # original image size
	if returnJson:
		returnJson["Height"] = H_orig;
		returnJson["Width"] = W_orig;
	# create grayscale version of image (just for displaying)
	img_lab_bw = img_lab.copy()
	img_lab_bw[:,:,1:] = 0
	img_rgb_bw = color.lab2rgb(img_lab_bw)
	scipy.misc.imsave(os.path.join(app.config['OUTPUT_FOLDER'],"bw_proc_"+filename),img_rgb_bw);

	# resize image to network input size
	global H_in
	global W_in
	img_rs = caffe.io.resize_image(img_rgb,(H_in,W_in)) # resize image to network input size
	img_lab_rs = color.rgb2lab(img_rs)
	img_l_rs = img_lab_rs[:,:,0]

	# show original image, along with grayscale input to the network
	img_pad = np.ones((H_orig,W_orig/10,3))

	net.blobs['data_l'].data[0,0,:,:] = img_l_rs-50 # subtract 50 for mean-centering
	net.forward() # run network

	ab_dec = net.blobs['class8_ab'].data[0,:,:,:].transpose((1,2,0)) # this is our result
	ab_dec_us = sni.zoom(ab_dec,(1.*H_orig/H_out,1.*W_orig/W_out,1)) # upsample to match size of original image L
	img_lab_out = np.concatenate((img_l[:,:,np.newaxis],ab_dec_us),axis=2) # concatenate with original image L
	img_rgb_out = np.clip(color.lab2rgb(img_lab_out),0,1) # convert back to rgb
	scipy.misc.imsave(os.path.join(app.config['OUTPUT_FOLDER'],"color_proc_"+filename),img_rgb_out);


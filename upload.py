from flask import *  
import os
from werkzeug.utils import secure_filename
import urllib.request
import shutil
import demo 
app = Flask(__name__)  
app.secret_key = "secret key"
SRC = ''
ALLOWED_EXTENSIONS = set(['mp4', '3gp', 'mpeg'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/final')
def final_page():
	return render_template('success.html', value=app.config['SRC'])

@app.route('/process')
def script_call():
	return redirect(demo.main(app.config['SRC']))

@app.route('/download')
def file_download():
	path="D:/Degree/6th Sem/Data Mining and Analysis(practical)/YOLOv3-master/videos/res/"+app.config['SRC']
	return send_file(path, as_attachment=True)

@app.route('/success', methods=['POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(filename)
			shutil.copy(filename, 'D:/Degree/6th Sem/Data Mining and Analysis(practical)/YOLOv3-master/videos/test')
			app.config['SRC']=filename
			os.remove(filename)
			flash('File successfully uploaded')
			return redirect('/process')
		else:
			flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
			return redirect(request.url)

if __name__ == "__main__":
    app.run()
   
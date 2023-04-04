from flask import Flask, Response,render_template,request,flash,url_for,redirect,session
import cv2
import os
from detector import Detector
from forms import IPCamForm
import time

STATIC_FOLDER='static'

app = Flask(__name__,)

app.config['STATIC_FOLDER'] = STATIC_FOLDER
app.secret_key =str(os.urandom(12))


ipcam_url = ""

fps=0
showResult = False

input_frame = []

detector = Detector()


def detect_with_ipcam():
    global showResult
    try:
        colors = [[0,255,0],[0,0,255],[0,255,255]]
        
        while showResult:    
            global input_frame
            if fps%15==0 and input_frame!=[]:
                
                ret, buffer = cv2.imencode('.jpg', detector.detect(input_frame,colors ))
                output = buffer.tobytes()

                
                yield  (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + output + b'\r\n')
            else:
                continue
    except:
        flash("Detection error")
        return render_template("mainPage.html")


def gen_frames(): 
    global showResult
    try:
        for i in range(10):  
            print("Tekrar bağlanılıyor...")
            time.sleep(5)

            cap = cv2.VideoCapture(ipcam_url)
        
            while showResult:
                
                success, cam_frame = cap.read()  # read the camera frame
                
                global input_frame
                input_frame = cam_frame
                
                global fps
                fps+=1
                
                if not success:
                
                    break

                else:
                    ret, buffer = cv2.imencode('.jpg', cam_frame)
                    cam_frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + cam_frame + b'\r\n')  # concat frame one by one and show result
        
 
    except :
        with app.app_context(), app.test_request_context():
            flash("Camera link error.Image None")


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
@app.route('/output_feed')
def output_feed():
    return Response(detect_with_ipcam(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/result',methods=["GET","POST"])
def result():
    global showResult
    showResult = request.args.get("showResult")
    
    

    if request.method == 'POST'  :
        
        if showResult=="True":
            detector.loadModel()
        
        showResult = request.args.get("showResult")

        return  redirect(url_for("result",showResult=showResult)) 
  
    return render_template("result_page.html",showResult=showResult) 

@app.route('/',methods=['POST',"GET"])
def home():
    global ipcam_url 
    global showResult 
    global fps 
    form = IPCamForm(request.form)
    if request.method == 'POST'  and form.validate():
      
        ipcam_url = form.url.data

        
        fps=0
        showResult = False
        flash("System working...")
        return  redirect(url_for("result",showResult=showResult)) 
    
    
    else:
        showResult=False
        session.clear()
        ipcam_url = ""

    return render_template("mainPage.html",form=form,showResult=showResult) 
    
        
if __name__ == '__main__':
    
    app.run(debug=True,host='0.0.0.0',port=5000)
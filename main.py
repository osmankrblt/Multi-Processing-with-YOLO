import cv2
from detector import Detector
from multiprocessing import Process
import time

def gen_frames(url,win_name): 
   
    try:
        
        frame_number = 0
        
        detector = Detector()
        detector.loadModel()

        print("Model yüklendi...")

        for i in range(10):  
            print("Bağlanılıyor...")
            
            time.sleep(5)
            
          

            cap = cv2.VideoCapture(url)
            ret =True
            while ret:
                
                ret, cam_frame = cap.read()  # read the camera frame
                cam_frame = cv2.resize(cam_frame,(480,360))
                
                
                if not ret:
                
                    break

                elif frame_number%30 == 0:
                    result = detector.detect(cam_frame,[0,0,255])

                    frame_number = 0

                    cv2.imshow(str(win_name),result)
                    cv2.waitKey(1)

                frame_number +=1
        
 
    except Exception as e:
       print("Error gen frames "+ str(e))





if __name__ == '__main__':
    
    
    
    
    p1 = Process(target=gen_frames,args=("http://192.168.0.103:8080/video","1",))
    p2 = Process(target=gen_frames,args=("http://192.168.0.103:8080/video","2",))
   


    p1.start()
    p2.start()
    

    p1.join()
    p2.join()
import cv2
import random
import torch



class Detector():
    def __init__(self):
        self.model=None

    def loadModel(self):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
       
        
        
        self.model = torch.hub.load('yolov7', 'custom', "bestv3.pt",source="local",
                        force_reload=True, trust_repo=True).to(self.device) if self.model == None  else self.model
        
     

    
    def plot_one_box(self,x, img, color=None, label=None, line_thickness=3):
        # Plots one bounding box on image img
        tl = line_thickness or round(0.005 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
        color = color or [random.randint(0, 255) for _ in range(3)]
        c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
        cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
        
        tf = max(tl - 1, 1)  # font thickness
        """
        # This code write the "EGEROBOT - isgsis"

        
        my_t_size = cv2.getTextSize("EGEROBOT - isgsis", 0, fontScale=tl / 3, thickness=tf)[0]
        
        my_c2 = c1[0] + my_t_size[0], c2[1] + my_t_size[1] + 3
        cv2.rectangle(img, (c1[0],c2[1]), my_c2, [0,0,0], -1, cv2.LINE_AA)
        cv2.putText(img, "EGEROBOT - isgsis", (c1[0],c2[1]+9), 0, tl / 3, [225, 255, 255], lineType=cv2.LINE_AA)

        # This code write the "EGEROBOT - isgsis"
        """

        if label:
        
            t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
            c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
            cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
            textColor = [255,255,255] if color == [0,0,255] else [0,0,0]

            cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, textColor, thickness=tf, lineType=cv2.LINE_AA)

        return img

    def detect(self,image,colors,TABLE_CONFIDENCE=0.7):
        
        results = self.model(image)
           
     
    
        # Bounding Boxes color scheme
        
        
        df = results.pandas().xyxy[0]
    
    
        for _, row in df.iterrows():
            if  row['confidence'] > TABLE_CONFIDENCE:
            
                bbox = [int(row['xmin']), int(row['ymin']),
                                    int(row['xmax']), int(row['ymax'])]
                label = row["name"]
                cls = row["class"]
                image = self.plot_one_box(bbox,image,label=label,color=colors[int(cls)])
            

        return image
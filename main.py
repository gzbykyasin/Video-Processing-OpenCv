import cv2
import numpy as np
import time


#print(request)
kamera=cv2.VideoCapture("kayit.mp4")
nesne=cv2.imread('resis.png',0)

frame_width = int(kamera.get(3))
frame_height = int(kamera.get(4))
#out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('X','V','I','D'), 10, (frame_width,frame_height))

w,h=nesne.shape[::-1]
#kamera.set(cv2.CAP_PROP_FRAME_HEIGHT,600)
#kamera.set(cv2.CAP_PROP_FRAME_WIDTH,1200)
gelen=0
sayi=0

def resim_isleri(params):

    parametre=cv2.cvtColor(params,cv2.COLOR_BGR2GRAY)
    th3 = cv2.adaptiveThreshold(parametre, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 11)
    #nesne3 = cv2.adaptiveThreshold(nesne, 250, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 23, 13)
    blur=cv2.GaussianBlur(th3,(7,7),11)
    _, thres1 = cv2.threshold(parametre, 100, 255, cv2.THRESH_TRUNC)
    koor=kose_bul(th3)

    return koor

def kose_bul(thres_eslestir):

    res = cv2.matchTemplate(thres_eslestir, nesne, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(frame, top_left, bottom_right, (0, 10, 250), 2)
    #cv2.circle(frame,(100,100),50,(255,0,0),3)

    return max_loc

while True:

    req,frame=kamera.read()
    if req==True:
        font = cv2.FONT_HERSHEY_SIMPLEX
        koordinat= resim_isleri(frame)

        if koordinat[1] > 133 and koordinat[0]> 132:
            gelen = gelen + 1
            if gelen%3==0:
                sayi+=1
                cekilenler = 'resimler' + str(sayi) + '.png'
                cv2.putText(frame, 'Basarili', (40, 150), font, 2, (0, 200, 0), 3, cv2.LINE_AA)
                cv2.imwrite(cekilenler, frame)
                time.sleep(0.1)
                print(min)

        else:
            gelen=gelen
        cv2.putText(frame, 'Urunler:', (40, 40), font, 2, (0, 200, 0), 3, cv2.LINE_AA)
        cv2.putText(frame, '{}'.format(sayi), (290, 40), font, 2, (0, 200, 0), 3, cv2.LINE_AA)
        cv2.imshow('Orjinal Goruntu',frame)
        #cv2.imshow('th3',min)
        #out.write(frame)
        if cv2.waitKey(10) & 0xFF==ord('q'):
            break
    else:
        print("Kamera acilmadi")
        break

kamera.release()
#out.release()
cv2.destroyAllWindows()
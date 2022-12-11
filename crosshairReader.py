import scipy
from scipy import ndimage
import numpy as np
import imageio.v3 as imageio
import matplotlib.pyplot as plt
import time
import statistics


def show(image):
    if True:
        plt.imshow(image)
        plt.ion()
        plt.gray()
        plt.show()
        plt.pause(1)


def displacement(a,b):
    return (b[1]-a[1],b[0]-a[0])
    

def findCrosshairCenter(frame,crosshairKernel,smoothKernel,printTimes=False,showImgs=False):
    #boi = np.sum(imageio.imread(filename),2)
    #time1=time.time()
    
    boi=frame#np.sum(frame,2)
    boi=boi*0.1 + 128
    #time2=time.time()
    
    #show(boi)

    gaussed=ndimage.gaussian_filter(boi, 1)
    #time3=time.time()
    
    #show(gaussed)

    sx = ndimage.sobel(gaussed,axis=0)
    sy = ndimage.sobel(gaussed,axis=1)
    sob = np.hypot(sx, sy)
    #time4=time.time()
    
    #show(sob)

    smoothed=np.clip(ndimage.convolve(sob, smoothKernel,mode='constant',cval=128),0,1000)
    #time5=time.time()
    
    #show(smoothed)

    binerized=smoothed>np.percentile(smoothed, 92)
    binerized=binerized*0.05
    #time6=time.time()
    
    #show(binerized)

    crosshairID=ndimage.convolve(binerized, crosshairKernel,mode='constant',cval=0)
    crosshairID=ndimage.gaussian_filter(crosshairID, 2)
    #time7=time.time()
    
    show(crosshairID)

    #print(np.percentile(crosshairID,99.94))
    centerImg=crosshairID>=np.percentile(crosshairID, 99.98)
    #time8=time.time()

    #print(ndimage.center_of_mass(centerImg))
    #show(centerImg)

    CoM=ndimage.center_of_mass(centerImg)

    x,y=CoM
    x=int(x)
    y=int(y)

    region=40
    newCenterImg=centerImg[x-region:x+region,y-region:y+region]
    CoM=ndimage.center_of_mass(newCenterImg)
    
    if showImgs:
        fig, ((a,b),(c,d)) = plt.subplots(2,2)
        plt.gray()
        a.imshow(boi)
        b.imshow(sob)
        c.imshow(crosshairID)
        d.imshow(centerImg)
        plt.plot(CoM[1]+y-region, CoM[0]+x-region, marker='+', color="red")
        plt.show()

    
    if printTimes:
        print("Flatten: ",time2-time1)
        print("Gaussian: ",time3-time2)
        print("Sobel: ",time4-time3)
        print("Smooth: ",time5-time4)
        print("Binerize: ",time6-time5)
        print("Crosshair Convolution: ",time7-time6)
        print("Crosshair Center: ",time8-time7)
        

    return (CoM[1]+y-region, CoM[0]+x-region)


#a=findCrosshairCenter(input("enter filename: "))


crosshairKernel=[]
with open('kernelLite.txt','r') as crosshairKernelFile:
    for line in crosshairKernelFile:
        newLine=[]
        vals=line.split()
        for val in vals:
            newLine.append(int(val))
        crosshairKernel.append(newLine)
crosshairKernel=0.001*np.array(crosshairKernel)

#smoothKernel=0.1*np.array([[0,0,1,0,0],[0,0,0,0,0],[1,0,0,0,1],[0,0,0,0,0],[0,0,1,0,0]])
smoothKernel=0.1*np.array([[0,1,0],[1,0,1],[0,1,0]])


start=time.time()
xPoses=[]
yPoses=[]
framesToAvg=[]
avgNum=5
for frame_count, frame in enumerate(imageio.imiter("<video1>")):
    #print(frame_count)
    #framesToAvg.append(np.sum(frame,2))
    framesToAvg.append(ndimage.zoom(frame[:,:,1],0.25))
    if (frame_count+1)%avgNum==0:
        realImage=np.average(framesToAvg,axis=0)
        framesToAvg=[]
    else:
        continue
    imageLoaded=time.time()
    pos=findCrosshairCenter(realImage,crosshairKernel,smoothKernel)
    try:
        posMod=(int(pos[0]),int(pos[1]))
        print(posMod)
        xPoses.append(int(pos[0]))
        yPoses.append(int(pos[1]))
    except:
        print("NO CROSSHAIR FOUND")
    #time.sleep(0.5)

    #print("Loading: ", imageLoaded-start)
    #print("Processing: ",processed-imageLoaded)

    
    start=time.time()
    #time.sleep(1)
#b=findCrosshairCenter('b.jpg')
#print(displacement(a,b))



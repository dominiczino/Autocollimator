import scipy
from scipy import ndimage
import numpy as np
import imageio.v3 as imageio
import matplotlib.pyplot as plt
import time
import statistics
import json


class kernelGenerator():
    def __init__(self):
        pass

    def generateCrosshairKernel(self,size,linewidth):
        if linewidth%2==0:
            raise ValueError("Linewidth must be an odd integer")
        if (size-linewidth)%2==1:
            raise ValueError("Size minus linewidth must be an even number")
        
        sides=int((size-linewidth)/2)
        kernel=[]
        for x in range(sides):
            line=[0 for i in range(sides)]
            line+=[1 for i in range(linewidth)]
            line+=[0 for i in range(sides)]
            kernel.append(line)
        for x in range(linewidth):
            kernel.append([1 for i in range(size)])
        for x in range(sides):
            line=[0 for i in range(sides)]
            line+=[1 for i in range(linewidth)]
            line+=[0 for i in range(sides)]
            kernel.append(line)
        return kernel

    def generateSmoothKernel(self,size):
        if size%2==0:
            raise ValueError("Size must be odd")

        sides=int((size-1)/2)
        kernel=[[0 for i in range(size)] for j in range(size)]
        kernel[0][sides]=1
        kernel[sides][0]=1
        kernel[sides][size-1]=1
        kernel[size-1][sides]=1
        return kernel
            

class CrosshairDetector():
    def __init__(self):
        pass

    def loadParameters(self,paramDict):
        self.params=paramDict

    def show(self,image):
        if True:
            plt.imshow(image)
            plt.ion()
            plt.gray()
            plt.show()
            plt.pause(1)

    def findCrosshairCenter(self,image,crosshairKernel,smoothKernel,printTimes=False,showImgs=False,easy=False):
        time1=time.time()
        totalX,totalY=image.shape
    



        if easy:
            #print(np.percentile(image,99))
            centerImg=image>90
        else:
            #Normalize the incoming image to prevent saturation
            initial=image*0.1 + 128 
            time2=time.time()
            
            #Gaussian blur to remove basic sensor noise
            gaussed=ndimage.gaussian_filter(initial, self.params["GAUSSIAN_SIGMA"]) 
            time3=time.time()

            #Sobel Filter detects the edges of the crosshairs
            sx = ndimage.sobel(gaussed,axis=0)
            sy = ndimage.sobel(gaussed,axis=1)
            sob = np.hypot(sx, sy)
            time4=time.time() 
            
            #This kernel is inteded to "fill in" the area between the two crosshair edges
            smoothed=np.clip(ndimage.convolve(sob, smoothKernel,mode='constant',cval=128),0,500)
            time5=time.time()

            #Extract the crosshairs themselves
            binerized=smoothed>np.percentile(smoothed, self.params["CROSSHAIR_PERCENTILE"]) #92
            binerized=binerized*0.05
            time6=time.time()

            #Applies the crosshair identifying kernel, which should highlight the centerpoint
            crosshairID=ndimage.convolve(binerized, crosshairKernel,mode='constant',cval=0)
            crosshairID=ndimage.gaussian_filter(crosshairID, 2)
            time7=time.time()

            #Extract the most bright pixels, hopefully just the center
            perc=100-100*self.params["CENTER_PIXELS"]/(totalX*totalY)
            centerImg=crosshairID>=np.percentile(crosshairID, perc) #99.98
            #centerImg=crosshairID>=np.percentile(crosshairID, self.params["CENTER_PERCENTILE"]) #99.98
            time8=time.time()

        

        #Find rough center of mass. This value may be swung around by outliers and noise
        x,y=ndimage.center_of_mass(centerImg)

        if easy:
            CoM = (x,y)
            xCom,yCom=CoM
        else:
            #Crop out an area around the estimated center of mass
            xPix=int(x)
            yPix=int(y)

            focusedSearchRadius=self.params["REFINEMENT_RADIUS"]
            xLower=max(0,xPix-focusedSearchRadius)
            xUpper=min(xPix+focusedSearchRadius,totalX-1)
            yLower=max(0,yPix-focusedSearchRadius)
            yUpper=min(yPix+focusedSearchRadius,totalY-1)
            newCenterImg=centerImg[xLower:xUpper, yLower:yUpper]

            #Get a new center of mass estimate based on that cropped region. If there were no outliers, this shold be the same.
            xNew,yNew=ndimage.center_of_mass(newCenterImg)
            CoM=(xNew+xPix-focusedSearchRadius, yNew+yPix-focusedSearchRadius)
            xCom,yCom=CoM

        if showImgs:
            if easy:
                fig, (a,b) = plt.subplots(1,2)
                plt.gray()
                a.imshow(image)
                b.imshow(centerImg)
                b.plot(yCom,xCom, marker='+', color="red")
            else:
                fig, ((a,b,c),(d,e,f)) = plt.subplots(2,3)
                plt.gray()
                a.imshow(initial)
                b.imshow(sob)
                c.imshow(smoothed)
                d.imshow(binerized)
                e.imshow(crosshairID)
                f.imshow(centerImg)
                f.plot(yCom,xCom, marker='+', color="red")
            
            plt.show()

        if printTimes:
            print("Flatten: ",time2-time1)
            print("Gaussian: ",time3-time2)
            print("Sobel: ",time4-time3)
            print("Smooth: ",time5-time4)
            print("Binerize: ",time6-time5)
            print("Crosshair Convolution: ",time7-time6)
            print("Crosshair Center: ",time8-time7)

        return CoM

################################################################################
################################################################################
################################################################################
################################################################################
################################################################################




params=dict()
with open("params.json") as f:
    params=json.load(f)

kernelgen=kernelGenerator()
crosshairKernel=0.001*np.array(kernelgen.generateCrosshairKernel(params["CROSSHAIR_KERNEL_SIZE"],params["CROSSHAIR_WIDTH"]))
smoothKernel=kernelgen.generateSmoothKernel(params["SMOOTH_KERNEL_SIZE"])


frameBuffer=[]
detector=CrosshairDetector()
detector.loadParameters(params)






badInput=True
while badInput:
    val="thou"#input("Select Units: \n\tum: Microns per 100mm \n\tas: arcseconds\n\t-->")
    if val=="um":
        calFactor=params['MICRON_PER_100MM']
        print("\n\n\tUNITS ARE MICRON PER 100mm")
        print("\t\tFull range is +/- 370")
        badInput=False
    elif val=="as":
        calFactor=params['ARCSECONDS']
        print("\n\n\tUNITS ARE ARCSECONDS")
        print("\t\tFull range is +/- 1020\"")
        badInput=False
    elif val=="thou":
        calFactor=1/3.455
        badInput=False

N=params["AVERAGE_WINDOW"]

xVals=[0 for i in range(N)]
yVals=[0 for i in range(N)]

for frame_count, frame in enumerate(imageio.imiter("<video0>")):
    #frameBuffer.append(  ndimage.zoom(  np.sum(frame,2), params["RESCALE_FACTOR"]  )  )
    frameBuffer.append(  ndimage.zoom(  frame[:,:,1], params["RESCALE_FACTOR"]  )  )
    #frameBuffer.append(  ndimage.zoom(  frame, (0.5,0.5,1)  )  )
    
    if (frame_count+1)%params["FRAMES_TO_AVERAGE"]==0:
        realImage=np.average(frameBuffer,axis=0)
        frameBuffer=[]
    else:
        continue
    
    pos=detector.findCrosshairCenter(realImage,crosshairKernel,smoothKernel,showImgs=False,easy=True)
        

    x=(pos[1]-400)*calFactor
    y=-(pos[0]-300)*calFactor
    
    xVals.append(x)
    yVals.append(y)
    xVals.pop(0)
    yVals.pop(0)
    
    try:
        posMod=(round(sum(xVals)/N,2),round(sum(yVals)/N,2))
        print(posMod)
    except:
        print("NO CROSSHAIR FOUND")
#    break



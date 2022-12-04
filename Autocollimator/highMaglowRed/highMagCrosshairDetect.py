import scipy
from scipy import ndimage
import numpy as np
import imageio.v2 as imageio
import matplotlib.pyplot as plt


def show(image):
    if True:
        plt.imshow(image)
        plt.gray()
        plt.show()


def displacement(a,b):
    return (b[1]-a[1],b[0]-a[0])
    


def findCrosshairCenter(filename):
    boi = np.sum(imageio.imread(filename),2)
    boi=boi*0.1 + 128
    show(boi)


    gaussed=ndimage.gaussian_filter(boi, 1)
    show(gaussed)


    sx = ndimage.sobel(gaussed,axis=0)
    sy = ndimage.sobel(gaussed,axis=1)
    sob = np.hypot(sx, sy)
    show(sob)

    smoothKernel=0.1*np.array([[0,0,1,0,0],[0,0,0,0,0],[1,0,0,0,1],[0,0,0,0,0],[0,0,1,0,0]])
    smoothed=np.clip(ndimage.convolve(sob, smoothKernel,mode='constant',cval=128),0,1000)
    show(smoothed)

    binerized=smoothed>np.percentile(smoothed, 92)
    #print(sum(sum(list(binerized))))
    binerized=binerized*0.1
    
    show(binerized)

    crosshairKernel=[]
    with open('crosshairDetect.txt','r') as crosshairKernelFile:
        for line in crosshairKernelFile:
            newLine=[]
            vals=line.split()
            for val in vals:
                newLine.append(int(val))
            crosshairKernel.append(newLine)
    crosshairKernel=0.001*np.array(crosshairKernel)
    crosshairID=ndimage.convolve(binerized, crosshairKernel,mode='constant',cval=0)
    show(crosshairID)

    centerImg=crosshairID>np.percentile(crosshairID, 99.90625)
    show(centerImg)

    return ndimage.center_of_mass(centerImg)


a=findCrosshairCenter('a.jpg')
b=findCrosshairCenter('b.jpg')
print(displacement(a,b))



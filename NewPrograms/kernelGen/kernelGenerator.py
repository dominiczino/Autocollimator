size = 25
lineWidth=3
distanceToLook=0
sides=int((size-lineWidth)/2)

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
            



boi=kernelGenerator()
print(boi.generateCrosshairKernel(7,3))

##with open('kernelLite.txt','w') as file:
##    for a in range(sides-distanceToLook):
##        for i in range(sides):
##            file.write("0 ")
##        for i in range(lineWidth):
##            file.write("1 ")
##        for i in range(sides):
##            file.write("0 ")
##        file.write("\n")
##    for b in range(distanceToLook):
##        for i in range(size):
##            file.write("0 ")
##        file.write("\n")
##    for b in range(lineWidth):
##        for i in range(sides-distanceToLook):
##            file.write("1 ")
##        for i in range(distanceToLook*2+lineWidth):
##            file.write("1 ")
##        for i in range(sides-distanceToLook):
##            file.write("1 ")
##        file.write("\n")
##    for b in range(distanceToLook):
##        for i in range(size):
##            file.write("0 ")
##        file.write("\n")
##    for c in range(sides-distanceToLook):
##        for i in range(sides):
##            file.write("0 ")
##        for i in range(lineWidth):
##            file.write("1 ")
##        for i in range(sides):
##            file.write("0 ")
##        file.write("\n")


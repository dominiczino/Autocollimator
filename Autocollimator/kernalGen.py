size = 50
lineWidth=3
distanceToLook=0
sides=int((size-lineWidth)/2)


with open('kernel2.txt','w') as file:
    for a in range(sides-distanceToLook):
        for i in range(sides):
            file.write("0 ")
        for i in range(lineWidth):
            file.write("1 ")
        for i in range(sides):
            file.write("0 ")
        file.write("\n")
    for b in range(distanceToLook):
        for i in range(size):
            file.write("0 ")
        file.write("\n")
    for b in range(lineWidth):
        for i in range(sides-distanceToLook):
            file.write("1 ")
        for i in range(distanceToLook*2+lineWidth):
            file.write("1 ")
        for i in range(sides-distanceToLook):
            file.write("1 ")
        file.write("\n")
    for b in range(distanceToLook):
        for i in range(size):
            file.write("0 ")
        file.write("\n")
    for c in range(sides-distanceToLook):
        for i in range(sides):
            file.write("0 ")
        for i in range(lineWidth):
            file.write("1 ")
        for i in range(sides):
            file.write("0 ")
        file.write("\n")


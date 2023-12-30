import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import zmq
import json

x = [0 for i in range(100)]
y = [0 for i in range(100)]



context=zmq.Context()
socket=context.socket(zmq.REP)
socket.bind('tcp://*:5555')


figure, ax = plt.subplots(figsize=(4,3))
line, = ax.plot(x, y)
plt.axis([0, 100, -1000, 1000])


def func_animate(i):
    x = np.linspace(0, 100, 100)
    newdata=json.loads(str(socket.recv(),'ascii'))
    socket.send(b'acknowledge')
    
    val=float(newdata['y'])
    print('got {}'.format(val))
    y.pop(0)
    y.append(val)
    ynp=np.array(y)
    #print(ynp)
    
    
    line.set_data(x, ynp)
    
    return line,




ani = FuncAnimation(figure,
                    func_animate,
                    frames=1000,
                    interval=1)

plt.show()

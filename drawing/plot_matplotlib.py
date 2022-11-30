import numpy as np
import os
import time
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

'''
4,000 points = about 3 sec
10,000 points = about 8 sec
30,000 points = about 30 sec
60,000 points = about 60 sec
80,000 points = about 120 sec
'''

file_path='plotdata.txt'

def main():
    print("Start")
    time_start=time.time()

    # Setting
    global fig, ax
    fig = plt.figure(figsize=(5,8))
    ax = fig.add_subplot(111, projection='3d')
    graph_items(ax)

    # Plot
    plot(file_path, time_start)

    # Capture
    graph_capture(ax,fig, time_start)
    #graph_rotation(ax,fig,time_start)

    print("All complete.")


def plot(file_path, time_start):
    print(" --- Plot --- ")

    # File
    file=open(file_path,'r')
    n=sum([1 for _ in open(file_path)])
    print("-> Draw points: " + str(n))

    # Plot
    for i in range(n):
        if(i%4000==0):
            print(str(i) + "/" + str(n) + " -> " + str(i/n*100) + "%")
        x,y,z,r,g,b=file.readline(n).split()
        x=float(x)
        y=float(y)
        z=float(z)
        #color=(float(r),float(g),float(b))
        color=(float(r)/255,float(g)/255,float(b)/255)
        ax.scatter(x, y, z, color=color, s=1)

    time_now=time.time()-time_start
    print("Graph drawing completed (" + str(time_now) + " sec)")
    print(" ----------- ")


def graph_items(ax):
    # default setting
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['mathtext.fontset'] = 'stix'
    plt.rcParams["font.size"] = 9
    plt.rcParams['xtick.labelsize'] = 9
    plt.rcParams['ytick.labelsize'] = 9
    #plt.rcParams['ztick.labelsize'] = 9

    # axis
    plt.axis('off') #background
    xmin,xmax=-3,3
    ymin,ymax=-3,3
    zmin,zmax=0,10
    ax.set_xlim3d(xmin, xmax)
    ax.set_ylim3d(ymin, ymax)
    ax.set_zlim3d(zmin, zmax)

    # draw main axis
    ax.plot([xmin-0.5,xmax+0.5],[0,0],[0,0],'-',color='#000000',lw=0.5)
    ax.plot([0,0],[ymin-0.5,ymax+0.5],[0,0],'-',color='#000000',lw=0.5)
    ax.plot([0,0],[0,0],[zmin,zmax+0.5],'-',color='#000000',lw=0.5)

    # draw sub axis
    for num in range(-6,7):
        ax.plot([xmin,xmax],[num*0.5,num*0.5],[0,0],'-',color='#bbbbbb',lw=0.5)
        ax.plot([num*0.5,num*0.5],[ymin,ymax],[0,0],'-',color='#bbbbbb',lw=0.5)
        #ax.plot([0,0],[num,num],[zmin,zmax],'-',color='#bbbbbb',lw=0.5)
        #ax.plot([num,num],[0,0],[zmin,zmax],'-',color='#bbbbbb',lw=0.5)
    #for num in range(1,5):  
        #ax.plot([0,0],[ymin,ymax],[num*2.5,num*2.5],'-',color='#bbbbbb',lw=0.5)
        #ax.plot([xmin,xmax],[0,0],[num*2.5,num*2.5],'-',color='#bbbbbb',lw=0.5)
    ax.plot([xmin,xmax],[ymax,ymax],[zmax,zmax],'-',color='#bbbbbb',lw=0.5)
    ax.plot([xmin,xmax],[ymin,ymin],[zmax,zmax],'-',color='#bbbbbb',lw=0.5)
    ax.plot([xmax,xmax],[ymax,ymin],[zmax,zmax],'-',color='#bbbbbb',lw=0.5)
    ax.plot([xmin,xmin],[ymax,ymin],[zmax,zmax],'-',color='#bbbbbb',lw=0.5)
    ax.plot([xmin,xmax],[0,0],[zmax,zmax],'-',color='#bbbbbb',lw=0.5)
    ax.plot([0,0],[ymax,ymin],[zmax,zmax],'-',color='#bbbbbb',lw=0.5)
    
    # draw axis text
    ax.text(xmax+1,0,0,r"$x$ [mm]")
    ax.text(0,ymax+1,0,r"$y$ [mm]")
    ax.text(0,0,zmax+1,r"$z$ [mm]")
    ax.text(1,0,0,'10')
    ax.text(2,0,0,'20')
    ax.text(3,0,0,'30')
    ax.text(0,1,0,'10')
    ax.text(0,2,0,'20')
    ax.text(0,3,0,'30')
    ax.text(0,0,2,'20')
    ax.text(0,0,4,'40')
    ax.text(0,0,6,'60')
    ax.text(0,0,8,'80')
    ax.text(0,0,10,'100')


def graph_capture(ax,fig, time_start):
    print("graph capture...")

    dir = "./capture"
    if not os.path.exists(dir):
        os.makedirs(dir)

    ax.view_init(elev=15, azim=45)
    fig.savefig("capture/main_picture.png")

    for angle in range(4):
        print(str(angle) + "/4")

        ax.view_init(elev=0, azim=angle*90)
        fig.savefig("capture/picture_" + str(angle*90) + ".png")
        #plt.draw()
        #plt.pause(0.001)

        time_now=time.time()-time_start
        print("-> " + str(time_now) + " sec")

    print("Graph capture completed -> show ./capture")

    

def graph_rotation(ax,fig, time_start):
    print("graph rotation...")

    dir = "./rotation"
    if not os.path.exists(dir):
        os.makedirs(dir)

    for angle in range(0, 36):
        print(str(angle*10) + "/360")

        ax.view_init(elev=15, azim=angle)
        #plt.draw()
        #plt.pause(0.001)
        fig.savefig("rotation/picture_" + str(angle) + ".png")

        time_now=time.time()-time_start
        print("-> " + str(time_now) + " sec")

    print("Graph rotation completed -> show ./rotation")


if __name__ == '__main__':
    main()
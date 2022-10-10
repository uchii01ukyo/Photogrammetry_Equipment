import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def plot():
    # file
    file=open('plotvector1.txt','r')
    print('n=')
    n=int(input())

    fig, ax = plt.subplots(figsize = (7.5, 9))
    ax.grid()
    ax.set_xlim(75, 825)
    ax.set_ylim(-450, 450)

    arrow_dict = dict(arrowstyle = "->", color = "red")

    # plot
    for i in range(n):
        x,y,u,v=file.readline(n).split()
        x=float(x)
        y=float(y)
        u=float(u)
        v=float(v)
        #calc
        u=x+u*10
        v=y+v*10

        ax.annotate("", size = 5, color = "red",
                xy = (u, v), xytext = (x, y), arrowprops = arrow_dict)
        #plt.plot(x,y,clip_on=False,marker='+', color='red',markersize=3,markeredgecolor="red")

    plt.show()


def make():
    # file
    file_path='sampleplot.txt'

    file=open(file_path,'r')
    n=sum([1 for _ in open(file_path)])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    graph_items(ax)

    # plot
    for i in range(n):
        x,y,z,r,g,b=file.readline(n).split()
        x=float(x)
        y=float(y)
        z=float(z)
        color=(float(r),float(g),float(b))
        ax.scatter(x, y, z, color=color, s=1)

    plt.show()
    #ax.save_fig('test.png', bbox_inches="tight", pad_inches=0.05)


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
    ax.set_aspect('equal')

    # draw axis
    ax.plot([xmin,xmax],[0,0],[0,0],'-',color='#000000',lw=0.5)
    ax.plot([0,0],[ymin,ymax],[0,0],'-',color='#000000',lw=0.5)
    ax.plot([0,0],[0,0],[zmin,zmax],'-',color='#000000',lw=0.5)
    for num in range(-3,4):
        ax.plot([xmin,xmax],[num,num],[0,0],'-',color='#bbbbbb',lw=0.5)
        ax.plot([num,num],[ymin,ymax],[0,0],'-',color='#bbbbbb',lw=0.5)
        #ax.plot([0,0],[num,num],[zmin,zmax],'-',color='#888888',lw=0.5)
        #ax.plot([num,num],[0,0],[zmin,zmax],'-',color='#888888',lw=0.5)
    #for num in range(1,5):  
        #ax.plot([0,0],[ymin,ymax],[num*2.5,num*2.5],'-',color='#888888',lw=0.5)
        #ax.plot([xmin,xmax],[0,0],[num*2.5,num*2.5],'-',color='#888888',lw=0.5)
    ax.plot([xmin,xmax],[ymax,ymax],[zmax,zmax],'-',color='#bbbbbb',lw=0.5)
    ax.plot([xmin,xmax],[ymin,ymin],[zmax,zmax],'-',color='#bbbbbb',lw=0.5)
    ax.plot([xmax,xmax],[ymax,ymin],[zmax,zmax],'-',color='#bbbbbb',lw=0.5)
    ax.plot([xmin,xmin],[ymax,ymin],[zmax,zmax],'-',color='#bbbbbb',lw=0.5)
    
    # draw axis text
    ax.text(xmax,0,0,r"$x$")
    ax.text(0,ymax,0,r"$y$")
    ax.text(0,0,zmax,r"$z$")

if __name__ == '__main__':
    make()
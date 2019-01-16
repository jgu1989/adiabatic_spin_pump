#%matplotlib inline

import math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from numpy import linalg as LA
from scipy import linalg as LAs
from scipy.linalg import eig as eigscipy
import time
start_time = time.time()


global T,Eu,Ed,h,hz,wL,wR, a, b ,dchi,Tp,omega
#T=5e-3
#Ed=3.498
#Eu=3.441

T=10e-3
Ed=3.270
Eu=3.149
h=0e-3
hz=0

dchi=1e-6+0j

omega=1e6
Tp=2*math.pi/omega

#wL=1e9
#wR=1e9


def eigofH(hz,h):
    delta=8e-3
    nom=delta+hz+math.sqrt((hz+delta)**2/4+h**2)
    dem=2*h
    norm=math.sqrt(nom**2+dem**2)
    [a,b]=[nom/norm,dem/norm]
    return [a,b]

a=eigofH(hz,h)[0]
b=eigofH(hz,h)[1]






def geometric(muLC,muRC,amp):
	def fLinU(muL,muR):
	    f=1.0/(1.0+np.exp((Eu+hz/2.0-muL)/T))
	    return f
	
	def fLoutU(muL,muR):
	    f=1.0/(1.0+np.exp(-(Eu+hz/2.0-muL)/T))
	    return f
	
	def fRinU(muL,muR):
	    f=1.0/(1.0+np.exp((Eu+hz/2.0-muR)/T))
	    return f
	
	def fRoutU(muL,muR):
	    f=1.0/(1.0+np.exp(-(Eu+hz/2.0-muR)/T))
	    return f
	
    
	def H0(muL,muR):
	    H=np.zeros((2,2),dtype=complex)
	
	

	
	    Wp0L=wL*(fLinU(muL,muR)*a**2)
	    Wp0R=wR*(fRinU(muL,muR)*a**2)
	    
	    W0pL=wL*(fLoutU(muL,muR)*a**2)
	    W0pR=wR*(fRoutU(muL,muR)*a**2)
	   
	    W0p=W0pL+W0pR
	    Wp0=Wp0L+Wp0R
#	    e_chip=np.exp(1j*chip)
#	    e_chip2=np.exp(-1j*chip)
#	    e_chim=np.exp(1j*chim)
#	    e_chim2=np.exp(-1j*chim)



	    H[0,0]= -Wp0
	    H[0,1]=W0p
	    H[1,0]=Wp0
	    H[1,1]= -W0p
	    H=-H
	    
	#    print('0pL',W0pL)
	#    print('p0L',Wp0L)
	#    print('0pR',W0pR)
	#    print('p0R',Wp0R)
	#    print(H[0,1])
	#    print(H[1,0])
	    return H

	def H1U(muL,muR):
	    H=np.zeros((3,3),dtype=complex)
	
	    Wp0L=wL*(fLinU(muL,muR)*a**2)
	    Wp0R=wR*(fRinU(muL,muR)*a**2)
	    
	    W0pL=wL*(fLoutU(muL,muR)*a**2)
	    W0pR=wR*(fRoutU(muL,muR)*a**2)
	   
	    W0p=W0pL+W0pR
	    Wp0=Wp0L+Wp0R
#	    e_chip=np.exp(1j*chip)
#	    e_chip2=np.exp(-1j*chip)
#	    e_chim=np.exp(1j*chim)
#	    e_chim2=np.exp(-1j*chim)



	    H[0,0]= 0
	    H[0,1]=W0pR
	    H[0,2]=0
	    H[1,0]=-Wp0R
	    H[1,1]=0
	    H[1,2]=0
	    H[2,0]=0
	    H[2,1]=0
	    H[2,2]=0
	    H=-H
	    
	#    print('0pL',W0pL)
	#    print('p0L',Wp0L)
	#    print('0pR',W0pR)
	#    print('p0R',Wp0R)
	#    print(H[0,1])
	#    print(H[1,0])
	    return H
	    
	def fLinUdiff(muL,muR):
	    a=np.exp((Eu+hz/2.0-muL)/T)
#	    f=a/(1.0+a)**2.0/T
	    f=1.0/(1.0/a+2+a)/T
	    return f
	
	def fLoutUdiff(muL,muR):
	    a=np.exp((Eu+hz/2.0-muL)/T)
#	    f=-a/(1.0+a)**2.0/T
	    f=-1.0/(1.0/a+2+a)/T
	    return f
	
	def fRinUdiff(muL,muR):
	    a=np.exp((Eu+hz/2.0-muR)/T)
#	    f=a/(1.0+a)**2.0/T
	    f=1.0/(1.0/a+2+a)/T
	    return f
	
	def fRoutUdiff(muL,muR):
	    a=np.exp((Eu+hz/2.0-muR)/T)
#	    f=-a/(1.0+a)**2.0/T
	    f=-1.0/(1.0/a+2+a)/T
	    return f
	
	
	    


	

	def Hamilt(muL,muR,chip,chim):
	    H=np.zeros((2,2),dtype=complex)
	
	

	
	    Wp0L=wL*(fLinU(muL,muR)*a**2)
	    Wp0R=wR*(fRinU(muL,muR)*a**2)
	    
	    W0pL=wL*(fLoutU(muL,muR)*a**2)
	    W0pR=wR*(fRoutU(muL,muR)*a**2)
	   
	    W0p=W0pL+W0pR
	    Wp0=Wp0L+Wp0R
	    e_chip=np.exp(1j*chip)
	    e_chip2=np.exp(-1j*chip)
	#    e_chi=1.0+1j*chi
	#    e_chi2=1.0-1j*chi
	    H[0,0]= -Wp0
	    H[0,1]=W0pL+W0pR*e_chip
	    H[1,0]=Wp0L+Wp0R*e_chip2
	    H[1,1]= -W0p
	    H=-H
	    
	#    print('0pL',W0pL)
	#    print('p0L',Wp0L)
	#    print('0pR',W0pR)
	#    print('p0R',Wp0R)
	#    print(H[0,1])
	#    print(H[1,0])
	    return H	

	def HdiffL(muL,muR,chip,chim):
	    H=np.zeros((2,2),dtype=complex)
	
	    a=eigofH(hz,h)[0]
	    b=eigofH(hz,h)[1]
	
	    Wp0L=wL*(fLinUdiff(muL,muR)*a**2)
	    Wp0R=0
	    
	    W0pL=wL*(fLoutUdiff(muL,muR)*a**2)
	    W0pR=0
	   
	    W0p=W0pL+W0pR
	    Wp0=Wp0L+Wp0R
	    e_chip=np.exp(1j*chip)
	    e_chip2=np.exp(-1j*chip)
	#    e_chi=1.0+1j*chi
	#    e_chi2=1.0-1j*chi
	    H[0,0]= -Wp0
	    H[0,1]=W0pL+W0pR*e_chip
	    H[1,0]=Wp0L+Wp0R*e_chip2
	    H[1,1]= -W0p
	    H=-H
	    return H
	
	def HdiffR(muL,muR,chip,chim):
	    H=np.zeros((2,2),dtype=complex)
	
	    a=eigofH(hz,h)[0]
	    b=eigofH(hz,h)[1]
	
	    Wp0L=0
	    Wp0R=wR*(fRinUdiff(muL,muR)*a**2)
	    Wp0Ru=wR*(fRinUdiff(muL,muR)*a**2)
	    
	    W0pL=0
	    W0pR=wR*(fRoutUdiff(muL,muR)*a**2)
	    W0pRu=wR*(fRoutUdiff(muL,muR)*a**2)
	   
	    W0p=W0pL+W0pR
	    Wp0=Wp0L+Wp0R
	    e_chip=np.exp(1j*chip)
	    e_chip2=np.exp(-1j*chip)
	#    e_chi=1.0+1j*chi
	#    e_chi2=1.0-1j*chi
	    H[0,0]= -Wp0
	    H[0,1]=W0pL+W0pRu*e_chip
	    H[1,0]=Wp0L+Wp0Ru*e_chip2
	    H[1,1]= -W0p
	    H=-H
	    return H


	def F(muL,muR,chip,chim):
	#    H=Hamilt(t,chi)
	#    Hdagger=np.conj(H.transpose())
	#    print(H)
	#    print(Hdagger)
	
	    H=Hamilt(muL,muR,chip,chim)
	    A=eigscipy(H,left=True)
	    imin=A[0].argsort()[0]
	    imed=A[0].argsort()[1]
	    eig0=A[0][imin]
	    eig1=A[0][imed]
	    phi0R=A[2].transpose()[imin]
	    phi0L=A[1].transpose()[imin]
	    phi1R=A[2].transpose()[imed]
	    phi1L=A[1].transpose()[imed]
	    
	    phi0L=np.conj(phi0L)
	    phi1L=np.conj(phi1L)
	    
	    phi0L=phi0L/np.matmul(phi0L,phi0R)
	    phi1L=phi1L/np.matmul(phi1L,phi1R)

	#    phi1L=LA.eig(H1L_T)[1].transpose()[0]
	#    phi1L=np.conj(phi1L)
	
	#    print('eig of H1L',LA.eig(H1L))
	#    print('eig of H1L_T',LA.eig(H1L_T))
	#    print('left',phi1L)
	#    print('left from scipy',eigscipy(H1L,left=True))
	#    print('right',LA.eig(H1L)[1].transpose()[0])
	    
	    a=np.matmul(phi0L,HdiffL(muL,muR,chip,chim))
	    b1L=np.matmul(a,phi1R)
	    a=np.matmul(phi1L,HdiffR(muL,muR,chip,chim))
	    c1L=np.matmul(a,phi0R)
	    
	    a=np.matmul(phi0L,HdiffR(muL,muR,chip,chim))
	    b1R=np.matmul(a,phi1R)
	    a=np.matmul(phi1L,HdiffL(muL,muR,chip,chim))
	    c1R=np.matmul(a,phi0R)
	    
	    element1=(b1L*c1L-b1R*c1R)/((eig0-eig1))**2.0
	    
	    
	    intg=element1
	    return intg
	
	def BerryCurvature_U(muL,muR):
	#    BC=(-1j)*(integrand(muL,muR,dchi/2)-integrand(muL,muR,-dchi/2))/(dchi)
	    #BC=(-1j)*2*F(muL,muR,dchi/2)/(dchi)
	    print(temp1)

	    
	    BC_U=2*(temp1.imag)/(dchi)
#	    print("BC",BC_U)
	    return BC_U	

	def fmt(x, pos):
#  		a, b = '{:.2e}'.format(x).split('e')
#  		b = int(b)
#  		return r'${} \times 10^{{{}}}$'.format(a, b)
			return '{0:.1E}'.format(x).replace('+0', '').replace('-0', '-')
    
	def BC_plot1():
	    Ngrid=21 #41
	    xlist = np.linspace(Eu-50e-3, Ed+50e-3, Ngrid,endpoint=True)
	    ylist = np.linspace(Eu-50e-3, Ed+50e-3, Ngrid,endpoint=True)
	    X, Y = np.meshgrid(xlist, ylist)
	    BC_U=np.zeros((Ngrid,Ngrid),dtype=complex)
	    for i in range(Ngrid):
	        for j in range(Ngrid):
#	            BC_C[i,j]=(temp[0]+temp[1])
#	            BC_S[i,j]=(temp[0]-temp[1])
	            BC_U[i,j]=BerryCurvature_U(X[0][i],Y[j][0])
#	            BC_D[i,j]=(temp[1])

##### attention, the order of index


	    fig=plt.figure()

#	    p1=fig.add_subplot(221)
#	    cp = p1.contourf(X, Y, BC_C,128)
#	    plt.colorbar(cp,format=ticker.FuncFormatter(fmt))
#	    plt.title('(a) Charge')
#	    plt.xlabel('$\mu_L$ (eV)')
#	    plt.ylabel('$\mu_R$ (eV)')
#	    plt.gca().set_aspect('equal', adjustable='box')
#	    
#	    p2=fig.add_subplot(222)
#	    cp = p2.contourf(X, Y, BC_S,128)
#	    plt.colorbar(cp,format=ticker.FuncFormatter(fmt))
#	    plt.title('(b) Spin')
#	    plt.xlabel('$\mu_L$ (eV)')
#	    plt.ylabel('$\mu_R$ (eV)')
#	    plt.gca().set_aspect('equal', adjustable='box')

	    p3=fig.add_subplot(121)
	    cp = p3.contourf(X*1e3, Y*1e3, BC_U,16)
	    plt.colorbar(cp,format=ticker.FuncFormatter(fmt))
	    plt.title('(a) Up')
	    plt.xlabel('$\mu_L$ (meV)',fontsize=19)
	    plt.ylabel('$\mu_R$ (meV)',fontsize=19)
	    plt.xticks([0,50,100])
	    plt.yticks([0,50,100])

#	    plt.gca().set_aspect('equal', adjustable='box')

	    p4=fig.add_subplot(122)
	    cp = p4.contourf(X*1e3, Y*1e3, BC_U,16)
	    plt.colorbar(cp,format=ticker.FuncFormatter(fmt))
	    plt.title('(b) ')
	    plt.xlabel('$\mu_L$ (meV)',fontsize=19)
	    plt.ylabel('$\mu_R$ (meV)',fontsize=19)
	    plt.xticks([0,50,100])
	    plt.yticks([0,50,100])
#	    plt.gca().set_aspect('equal', adjustable='box')

	    plt.tight_layout()
	    plt.show()
	    return

	BC_plot1()

#	return current()
	return



wL=1e0
wR=1e0
muL=0
muR=0
#print(dynamic(muL,muR,0e-3)[0]*1.60217662*1e-4,dynamic(muL,muR,0e-3)[1]*1.60217662*1e-4)
print(geometric(muL,muR,0e-3))


#contour1()




print("time:", (time.time() - start_time)/60.0)



#x=[0,12,12,20,20,30]
#y=[0,0, 1e5*0.94,1e5*0.94,0,0]
#y2=[0,0, -1e5*0.94,-1e5*0.94,0,0]
#plt.plot(x,y)
#plt.plot(x,y2,'b--')
#
#plt.axhline(0)
#plt.xlabel('Center of chemical pot (mV)')
#plt.ylabel('Current')
#plt.legend(loc='upper left')
#plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
#plt.show()


######################################################
######################################################
######################################################

# delta/temperature

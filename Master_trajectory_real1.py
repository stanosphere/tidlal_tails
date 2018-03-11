from numpy import array, sqrt, sin, cos, pi, arctan
import numpy as np
import numpy.random as rand
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation

G = 1.0 #Newton's Constant
M = 1.0 #Mass of central object
M_p = 2.0 #Mass of perturbing galaxy
#creates a time array 
dt = 0.5
t = np.arange(0.0, 1000, dt)

def Trajectory_All(e,d,x0):
	def derivs(state, t):

		dydx = np.zeros_like(state)
		# dydx is the list of derivatives w.r.t. time

		dydx[0] = state[1]
		dydx[2] = state[3]
		dydx[4] = state[5]
		dydx[6] = state[7]
		dydx[8] = state[9]
		dydx[10] = state[11]
	
		r = sqrt((state[0] - state[6])**2 + (state[2] - state[8])**2 + (state[4] - state[10])**2)

		dydx[1] = -G*M*(state[0] - state[6])/(r**3)
		dydx[3] = -G*M*(state[2] - state[8])/(r**3)
		dydx[5] = -G*M*(state[4] - state[10])/(r**3)
		dydx[7] = -G*M_p*(state[6] - state[0])/(r**3)
		dydx[9] = -G*M_p*(state[8] - state[2])/(r**3)
		dydx[11] = -G*M_p*(state[10] - state[4])/(r**3)

		return dydx
	
	if e < 1:
		r_min = d
		a = r_min/(1-e) #semi-major axis
		r_max = 2*a - r_min 
		
		#I have chosen the initial conditions below such that the orbit begins @ r_max
		x = -r_max
		y = 0
		z = 0

		v_mag = sqrt((M*G/a)*((1-e)/(1+e)))
		
		vx = 0
		vy = v_mag
		vz = 0
		print('Ellipse!')
	elif e == 1:
		f = d #'focal lengh'
		x = x0
		y = 2*sqrt(f*(f-x0))
		z = 0 

		r = sqrt(x**2 + y**2 + z**2)

		v_mag = sqrt(2*M*G/r)
		theta = arctan(2*f/y) 

		vx = v_mag*cos(theta)
		vy = -v_mag*sin(theta)
		vz = 0
		print('Parabola!')
	elif e > 1:
		r0 = d*(e+1) #semi-latus rectum
		X = r0/(e**2 -1)
		Y = r0/(sqrt(e**2 - 1))
		xc = e*X
		theta = arctan(Y*(x0-xc)/(X*sqrt((x0-xc)**2 - X**2)))
		
		x = x0
		y = Y*sqrt(((x0-xc)**2/(X**2)) - 1)
		z = 0
		ri = sqrt(x**2 + y**2 + z**2) #initial radius
		v_mag = sqrt((2/ri + (e**2 - 1)/r0)*M*G)
		
		vx = v_mag*cos(theta)
		vy = v_mag*sin(theta)
		vz = 0
		print('Hyperbola!')
	#Initial conditions of original galaxy
	x_o = 0
	y_o = 0
	z_o = 0
	vx_o = 0
	vy_o = 0
	vz_o = 0

	#This just creates the initial conditions in a convenient format
	state=np.reshape(np.transpose(np.vstack((x,vx,y,vy,z,vz,x_o,vx_o,y_o,vy_o,z_o,vz_o))),12)
	#This bit does the integration
	r = integrate.odeint(derivs, state, t)
	return r

r=Trajectory_All(1.5,12,-20)
#1st argument is eccentricity: e=0 for circle, 0<e<1 for ellipse, e=1 for 
#parabola and e>1 for hyperbola.
#2nd argument is distance of closst approach (in case of M_p being very small)
#3rd argument is initial x displacement (should be -ve)

dim = np.shape(r) #first element gives number of time steps
n = dim[0]
galac_sep = np.zeros(n)
for j in range(0,n):
	galac_sep[j] = sqrt((r[j,0]-r[j,6])**2 + (r[j,2]-r[j,8])**2 + (r[j,4]-r[j,10])**2)
d_min = min(galac_sep)
print('The Distance of closest approach is: %s' %d_min)

fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-20, 20), ylim=(-20, 20))
ax.grid()
ax.plot(0,0,marker='o', color='r',markersize = 15)

line2, = ax.plot([], [], 'o',markersize=15)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

def init():
    line2.set_data([], [])
    time_text.set_text('')
    return line2, time_text

def animate(i):
	x_plot = [r[i,0],r[i,6]]
	y_plot = [r[i,2],r[i,8]]

	line2.set_data(x_plot, y_plot)
	time_text.set_text(time_template%(i*dt))
	return line2, time_text

ani2 = animation.FuncAnimation(fig, animate, np.arange(1, len(r)),
    interval=25, blit=True, init_func=init)

fig, ax1 = plt.subplots()
ax1.plot(r[:,0],r[:,2],label="Path of Perturbing Galaxy", c='r',lw=2)
ax1.plot(r[:,6],r[:,8],label="Path of Original Galaxy", c='b',lw=2)
ax1.set_xlabel("x position")
ax1.set_ylabel("y position")
ax1.set_title("Orbital Trajectories")
ax1.legend(loc="lower left")

plt.show()

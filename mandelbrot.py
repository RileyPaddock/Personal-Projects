import matplotlib.pyplot as plt

#get the next complex number in our secence
def next_z(z,c):
  return add_cmplx(square(z), c)

#return the square of a complex number
def square(z):
  return [(z[0]**2)-(z[1]**2), 2*z[0]*z[1]] 

#add 2 complex numbers
def add_cmplx(z,c):
  return [z[0]+c[0], z[1]+c[1]]

#find the distance of a complex number from the origin
def distance(z):
  return ((z[0]**2) + (z[1]**2))**(0.5)

#for a given function, check if our function diverges or converges
def check_inclusion(c):
  for i in range(1000):
    if i == 0: z_old = [0,0]
    z_n = next_z(z_old,c)
    z_old = list(z_n)
    if distance(z_n) > 2:
      #if we are every more than 2 units away from the origin, we diverge
      return False
  else:
      return True


#for every number on our grid, down to 0.01 specificity, check if our function diverges or converges
#If it converges color the pixel black, if it diverges then color it white.
count = 0
total = 400**2
for x in range(400):
  for y in range(400):
    count += 1
    print(str((count/total)*100)+"%", end="\r")
    if check_inclusion([(x-200)/100,(y-200)/100]):
      plt.plot((x-200)/100, (y-200)/100, 'ok', markersize=1)
# plt.plot(0, 0, 'ok', markersize=1)
# plt.plot(0.001, 0, 'ok', markersize=1)
# plt.axis([-2, 1, -2, 2])
plt.savefig("test.png")

import matplotlib.pyplot as plt

def generate_slope_field(d_dx, x_range, y_range,line_len = 0.25):
    plt.style.use('bmh')
    #iterate through all points in our bounds
    for x in range(x_range[0],x_range[1]+1):
        for y in range(y_range[0],y_range[1]+1):
            #find the slope of the line at our point
            slope = d_dx(x,y)

            #find bounds for each line segment to ensure they are all the same length
            buffer = line_len/2
            x_buffer = (buffer/(1+slope**2))**(0.5)
            y_buffer = slope*x_buffer
            #account for axis being different sizes
            y_buffer *= (y_range[1] - y_range[0])/(x_range[1]-x_range[0])

            #plot the line segment
            plt.plot([x-x_buffer,x,x+x_buffer],[y-y_buffer,y,y+y_buffer])
    plt.savefig("images/slope_field.png")

def f(x,y):
    return x**2

generate_slope_field(f,(-10,10),(0,8))
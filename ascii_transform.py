from PIL import Image 

def convert_to_bw(filepath):#converts a given image to black and white
  img = Image.open(filepath)
  pixels = img.load()
  for x in range(img.size[0]):
    for y in range(img.size[1]):
      r,g,b = pixels[x,y];
      #finds brightness of pixel by treating (r,g,b) as (x,y,z) and finding distance from the origin
      result = round(255*(((r**2 + g**2 + b**2)/(3*(255**2)))**(0.5)))
      #normalize distance from the origin to some number between 0 and 255
      pixels[x,y] = (result,result,result)  # Set the RGBA Value of the image
  img.save('bw_'+filepath) 

def reduction(filepath,factor):#reduces the quality of an image by some given factor
  img = Image.open(filepath)
  pixels = img.load()
  #creates new blank image to color
  reduced_img = Image.new("RGB", (img.size[0]//factor,img.size[1]//factor), color=0)
  rdc_img_pxl = reduced_img.load()
  #divide the original image into boxed of some number of pixels
  for x in range(img.size[0]//factor):
    for y in range(img.size[1]//factor):
      #find the color of each pixel in our box 
      colors = [pixels[l,k] for k in range(y*factor,(y+1)*factor) for l in range(x*factor, (x+1)*factor)]
      num_pix = len(colors)
      #get the average color from all the pixels
      avg = tuple([sum([colors[i][j] for i in range(num_pix)])//num_pix for j in range(3)])
      #set the assosiated pixel in the reduced image to that average color
      rdc_img_pxl[x,y] = avg
  reduced_img.save(filepath[:-4]+"_rdc.jpg")
  return reduced_img
      



def ascii_transform(filepath):
  brightness = [" ",".",",","-","~",":",";","=","!","*","#","$","@"]
  result = ""
  img = Image.open(filepath)
  #specify how many characters wide we want our printout to be
  factor = img.size[0]//65
  #create a reduced image with our set width
  reduced_img = reduction(filepath,factor)
  pixels = reduced_img.load()
  #go through each pixel in our reduced image
  for y in range(reduced_img.size[1]):
    result += "\n"
    for x in range(reduced_img.size[0]):
      r,g,b = pixels[x,y]
      #take the rgb value of each pixel and treat as (x,y,z) and find distance from the open
      #normalize this distance to something between 0 and 12 and round to the nearest integer
      #brighter pixels will map to a smaller number, and darker ones to a larger
      index = round(12*(1-(((r**2 + g**2 + b**2)/(3*(255**2)))**(0.5))))
      #use the index to get an ascii character corresponding to how bright the pixel is and add to our result
      result += brightness[index]
  return result


print(ascii_transform("images/ascii/george_red_tounge.jpg"))
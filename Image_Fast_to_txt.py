from cmath import exp
from concurrent.futures import thread
from PIL import Image #pip install Pillow
import PIL
import cv2 # pip install opencv-python
import os
import sys, array, os, textwrap, math, random, argparse
from cgi import print_directory
from email.mime import image
from tkinter import W
import threading
import time

start_time = time.time()

## DA CODES ARE FROM : https://github.com/robertgallup/python-bmp2hex
def getLONG(a, n):
	return (a[n+3] * (2**24)) + (a[n+2] * (2**16)) + (a[n+1] * (2**8)) + (a[n])

def getINT(a, n):
	return ((a[n+1] * (2**8)) + (a[n]))

def reflect(a):
	r = 0
	for i in range(8):
		r <<= 1
		r |= (a & 0x01)
		a >>= 1
	return (r)

def getDoubleType (d):
	if d:
		dType = 'uint16_t' + ' *'
		dLen = 2
	else:
		dType = 'uint8_t' + ' *'
		dLen = 1

	return (dType, dLen)

def bmp2hex(infile, tablewidth, sizebytes, invert, raw, named, double, xbm):

	(pixelDataType, dataByteLength) = getDoubleType(double)

	tablename = os.path.splitext(infile)[0].upper()

	tablewidth = int(tablewidth) * 6

	outstring =  ''

	fin = open(infile, "rb")
	uint8_tstoread = os.path.getsize(os.path.expanduser(infile))
	valuesfromfile = array.array('B')
	try:
		valuesfromfile.fromfile(fin, uint8_tstoread)
	finally:
		fin.close()

	values=valuesfromfile.tolist()

	if ((values[0] != 0x42) or (values[1] != 0x4D)):
		sys.exit ("Error: Unsupported BMP format. Make sure your file is a Windows BMP.")

	dataOffset	= getLONG(values, 10)
	pixelWidth  = getLONG(values, 18)
	pixelHeight = getLONG(values, 22)
	bitDepth	= getINT (values, 28)
	dataSize	= getLONG(values, 34)

	byteWidth	= int(math.ceil(float(pixelWidth * bitDepth)/8.0))
	paddedWidth	= int(math.ceil(float(byteWidth)/4.0)*4.0)

	if (sizebytes==0):
		if (pixelWidth>255) or (pixelHeight>255):
			sizebytes = 2
		else:
			sizebytes = 1

	invertbyte = 0xFF if invert else 0x00
	if (bitDepth == 1):
		invertbyte = invertbyte ^ 0xFF

	if (raw):
		print ('PROGMEM unsigned char const ' + tablename + ' [] = {')
		if (not (sizebytes%2)):
			print ("{0:#04X}".format((pixelWidth>>8) & 0xFF) + ", " + "{0:#04X}".format(pixelWidth & 0xFF) + ", " + \
		    	  "{0:#04X}".format((pixelHeight>>8) & 0xFF) + ", " + "{0:#04X}".format(pixelHeight & 0xFF) + ",")
		else:
			print ("{0:#04X}".format(pixelWidth & 0xFF) + ", " + "{0:#04X}".format(pixelHeight & 0xFF) + ",")

	elif (named):
		print ('PROGMEM ' + getDoubleType(double)[0] + ' const ' + tablename + '_PIXELS[] = {')

	elif (xbm):
		print ('#define ' + tablename + '_width ' + str(pixelWidth))
		print ('#define ' + tablename + '_height ' + str(pixelHeight))
		print ('PROGMEM ' + getDoubleType(double)[0] + ' const ' + tablename + '_bits[] = {')

	else:
		pass
	fin.close()
	try:
		for i in range(pixelHeight):
			for j in range (byteWidth):
				ndx = dataOffset + ((pixelHeight-1-i) * paddedWidth) + j
				v = values[ndx] ^ invertbyte
				if (xbm):
					v = reflect(v)
				outstring += "{0:#04x}".format(v) + ", "

	finally:
		outstring = textwrap.fill(outstring[:-2], tablewidth)
		return outstring

##########################################################################################################################

img_list = []
bmp_count = 0
frame_count = 0
ascii_array = []

vidcap = cv2.VideoCapture('You Are My Angel !  KAWAI IKU NE !!.mp4')
success,images = vidcap.read()
count = 0

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

if int(major_ver)  < 3 :
	fps = vidcap.get(cv2.cv.CV_CAP_PROP_FPS)
else :
	fps = vidcap.get(cv2.CAP_PROP_FPS)

path = [os.path.join("./", "oled_TMP"),os.path.join("./oled_TMP", "pngs"),os.path.join("./oled_TMP", "bmps") ]
for i in path:
	try:
		os.mkdir(i)
	except:
		pass

def write_video(count, images):
	cv2.imwrite(".\\oled_TMP\\pngs\\frame%d.png" % count, images) 
	return



while success:
  success,images = vidcap.read()
  if success == False:
    break
  added_thread = threading.Thread(target = write_video, args=(count, images))
  added_thread.start() 
  print("????????????: " + str(count) + "???",success, end="\r")
  count += 1

added_thread.join()
print("??????????????????!                                          ")
vidcap.release()

for dirPath, dirNames, fileNames in os.walk("./oled_TMP/pngs"):
    for names in fileNames:
        img_list.append(names)
file_count = len(img_list)
print("??????: ", file_count, "?????????")

image_file = Image.open(f"./oled_TMP/pngs/{img_list[0]}")
width,height = image_file.size

if width / height > 2:
	height = round(height / (width / 128))
	width = 128
	xoffset = 0
	yoffset = round((64 - height) / 2)
elif width/height < 2:
	width =  round(width / (height / 64))
	height = 64
	xoffset = round((128 - width) / 2)
	yoffset = 0
else:
	width = 128
	height = 64
	xoffset = yoffset = 0 

def to_bmp(h):
  image_file = Image.open(f"./oled_TMP/pngs/{h}") # open colour image
  
  newsize = (width,height)
  
  imagecpy = image_file.resize(newsize)
  
  image_file.paste((0,0,0), [0,0,image_file.size[0],image_file.size[1]])
  default_size = (128,64) 
  new_image = image_file.resize(default_size)

  new_image.paste(imagecpy, (xoffset,yoffset))

  new_image = new_image.convert('1') # convert image to black and white

  new_image.save(f'./oled_TMP/bmps/{h[:-4]}.bmp')
  
  image_file.close()
  return

print("????????? png ????????? ??????bmp???...")
for i in img_list:
  ed_thread = threading.Thread(target = to_bmp, args=(i,))
  ed_thread.start() 
  bmp_count += 1
  print (f"[ {round(bmp_count / (file_count+1) * 100)}% ]" + " ??????: " + i + f" ({bmp_count+1} / {file_count})", end = "\r")
  
ed_thread.join()
print("[ 100% ] ??????!                                         ")

print("??????bmp????????? cpp ascii art ??????????????????...")

def make_ascii_art(frame_count):
	fn = ".\\oled_TMP\\bmps\\frame" + str(frame_count) + ".bmp"
	output = bmp2hex(fn, 16 , 0 , True, False, False, False, False)
	program = f"const unsigned char frame{frame_count} [] PROGMEM = " + "{\n" + output + "};\n\n"
	with open(f".\\codes\\frame{frame_count}.c", "a+") as file_object:
		file_object.write(program)


file_count = len(img_list)
for filename in sorted(img_list):
	print (f"[ {round(frame_count / (file_count+1) * 100)}% ]" + " ??????: " + filename[:-4] + f" ({frame_count+1} / {file_count})", end = "\r")
	ss = threading.Thread(target=make_ascii_art, args=(frame_count,))
	ss.start()
	frame_count += 1

ss.join()

l = ""
for i in range(0,frame_count):
    l += f"frame{i},"
    if i % 12 ==0:
        l += "\n"

program = f"const unsigned char* bitmap_allArray[{file_count}] = " + "{\n" + l + "};\n"

with open("main_array.txt", "a+") as file_object:
	file_object.write(program)

  
print("[ 100% ] ??????!                                         ")

print(f"??????: ", time.time() - start_time," s")


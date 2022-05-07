from PIL import Image
import os

img_list = []
frame_count = 0

print("開始擷取 pngs 資料夾中的png檔案...")
for dirPath, dirNames, fileNames in os.walk("./pngs"):
    for names in fileNames:
        img_list.append(names)
print("完成.")

print("開始將 png 檔轉成 單色bmp檔...")
for filename in img_list:
    image_file = Image.open(f"./pngs/{filename}") # open colour image
    image_file = image_file.convert('1') # convert image to black and white
    image_file.save(f'./bmps/{filename}.bmp')
print("完成.")

print("開始bmp檔轉成 cpp ascii art 並稱成程式碼...")

file_count = len(img_list)
for filename in img_list:
    print (f"[{frame_count} / {file_count}]" + "處理: " + filename)

    fn = ".\\bmps\\" + filename + ".bmp"
    stream = os.popen(f'python bmp2hex.py "{fn}"')
    output = (stream.read())
    with open(f"./codes/frame_{frame_count}.txt", "a+") as file_object:
        file_object.write(output)

    frame_count += 1



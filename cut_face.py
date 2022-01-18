# -*- coding:utf-8 -*-
import cv2
import os
import glob

# 使用する分類器のパス
cascade_path = 'haarcascade_frontalcatface_extended.xml'
faceCascade = cv2.CascadeClassifier(cascade_path)

# 使用する画像ディレクトリ名
name = ["***"]

# 切り抜いた画像の保存先ディレクトリを作成
os.makedirs("./imgs/"+str(name)+"_cut", exist_ok=True)
save_path = "./imgs/"+str(name)+"_cut/"
    
# 顔検知に成功した数(デフォルトで0を指定)
face_detect_count = 0
# 失敗した数
no_face_count = 0

files = glob.glob("imgs/" + str(name) + "/*")
print("{}の顔を検出し切り取りを開始します。".format(name))

for i, file in enumerate(files):
    all = os.path.basename(file)
    file_name = os.path.splitext(all)[0]
    img = cv2.imread(file, cv2.IMREAD_COLOR)
    if img is None:
        print('image' + str(i) + ':NoFace')
        no_face_count = no_face_count + 1
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face = faceCascade.detectMultiScale(gray, 1.04, 3)
        if len(face) > 0:
            for rect in face:
                x = rect[0]
                y = rect[1]
                w = rect[2]
                h = rect[3]
                cv2.imwrite(save_path + str(file_name) + 'cutted.jpg', img[y:y+h,  x:x+w])
                face_detect_count = face_detect_count + 1
     
    print("検出できた" + str(name) + "の数" + str(face_detect_count))
    print("検出できなかった" + str(name) + "の数" + str(no_face_count))

print("顔画像の切り取り作業、正常に動作しました。")


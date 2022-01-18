# -*- coding:utf-8 -*-
import cv2
import os
import glob



# OpenCVのデフォルトの分類器のpath。(https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xmlのファイルを使う)
cascade_path = '/Users/ayano/Downloads/neko_collector-main/neko_collector/haarcascade_frontalcatface_extended.xml'
# 例
#cascade_path = './opencv-master/data/haarcascades/haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascade_path)

SearchName = ["yancha"]



for name in SearchName:   
    # 画像データのあるディレクトリ
    input_data_path = glob.glob("/Users/ayano/Downloads/neko_collector-main/neko_collector/imgs/" + str(name))
    # 切り抜いた画像の保存先ディレクトリを作成
    os.makedirs("./Face/"+str(name)+"_newface2", exist_ok=True)
    save_path = "./Face/"+str(name)+"_newface2/"

    # 収集した画像の枚数(任意で変更)
    #image_count = 50
    
    # 顔検知に成功した数(デフォルトで0を指定)
    face_detect_count = 0
    # 失敗した数
    no_face_count = 0

    files = glob.glob("/Users/ayano/Downloads/neko_collector-main/neko_collector/imgs/" + str(name) + "/*")
    


    print("{}の顔を検出し切り取りを開始します。".format(name))
    # 集めた画像データから顔が検知されたら、切り取り、保存する。
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
                    # 顔認識部分を赤線で囲み保存(今はこの部分は必要ない)
                    # cv2.rectangle(img, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), (0, 0,255), thickness=1)
                    # cv2.imwrite('detected.jpg', img)
                    x = rect[0]
                    y = rect[1]
                    w = rect[2]
                    h = rect[3]
                    cv2.imwrite(save_path + str(file_name) + 'cutted.jpg', img[y:y+h,  x:x+w])
                    face_detect_count = face_detect_count + 1
            else:
                print('image' + str(i) + ':NoFace') 
                no_face_count = no_face_count + 1
                
    print("検出できた" + str(name) + "の数" + str(face_detect_count))
    print("検出できなかった" + str(name) + "の数" + str(no_face_count))


print("顔画像の切り取り作業、正常に動作しました。")


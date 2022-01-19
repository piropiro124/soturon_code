# soturon_code
卒論で使用したスクリプトファイルをまとめる

## img_collector.py
selemium、BeautifulSoup等を使用してスクレイピングを行なう

Dockerと繋げて使用した

## cut_face.py
画像から猫の顔を検出して切り抜き、保存する

参考サイト

https://qiita.com/yottyann1221/items/a08300b572206075ee9f

## make_data.py
データセットの前処理フェーズ

学習に使用する画像を訓練データ、テストデータに分けてNumpy配列で保存する

## neko_cross.py
学習フェーズ

交差検証を行なう仕様

正則化、転移学習モデルも記載


正則化参考サイト

https://www.tensorflow.org/tutorials/keras/overfit_and_underfit?hl=ja

転移学習参考サイト

https://www.tdi.co.jp/miso/study-deep-learning-3

## plot_results.py
学習結果グラフ表示フェーズ

訓練データとテストデータそれぞれの正解率と損失の推移がグラフで表示される

## same_search_ahash.py
ImageHashのaHashを利用してフォルダ内から重複した画像を検出する

## same_search_phash.py
ImageHashのpHashを利用してフォルダ内から重複した画像を検出する


ImageHashの参考サイト

https://tech.unifa-e.com/entry/2017/11/27/111546

https://water2litter.net/rum/post/python_imagehash_diff/

https://qiita.com/meznat/items/80c5ad8a893125db1941

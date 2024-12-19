# similar-Log

## 環境
Python-version:  
・Python 3.10.12  
使用VM構成：  
・cpu: 2コア  
・メモリ: 3GB  
・ストレージ: 25GB  

## 概要
任意のログデータを読み込み，条件に一致するログに対して，類似度計算を行うコード．
コード内では，テキストファイルに記入されたログに対して類似度計算を行っている．
プログラムを実行する際は，任意のログデータをlogs.txtに保存して使用する．

## 説明
### similar.py
読み込んだデータに対して，上から順にレーベンシュタイン距離の正規化を用いた，類似度計算を行う．
ここでは，ログを以下の７つのフィールドに分割している．
("objectID", "timestamp", "method", "server", "http_version", "status", "size")
コード内では，この中から比較を行うフィールドを定義している．
定義したフィールドは以下の通りである．
（"timestamp", "objectID", "http_version", "method", "status"）
また，serverに関しては，URLのパス部分を抽出して比較を行う．
この各フィールドを比較し類似度を算出する．
ファイルの読み込みでは，最初の1000行に対して処理を行っている．
出力として，0.1ずつの範囲で何件の類似しているログが何件かを表示する．


## 実行結果

![image](https://github.com/user-attachments/assets/ce2cf939-c970-426e-9971-02b56e80b802)
<p align="center">
・  
</p>   
<p align="center">
・  
</p>  
<p align="center">
・  
</p>  
![image](https://github.com/user-attachments/assets/651573f7-b923-47e8-986d-87c80729865d)


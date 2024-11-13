import streamlit as st

from Bio import SeqIO
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO # アップロードファイル操作用

def dotmatrix(f1, f2, win):
    # ファイルからの読み込み
    # 新型コロナウイルス（武漢型）の配列
    record1 = next(SeqIO.parse(f1, "fasta"))
    # SARS の配列
    record2 = next(SeqIO.parse(f2, "fasta"))

    # 配列の取り出し
    seq1 = record1.seq
    seq2 = record2.seq

    #win = 10
    len1 = len(seq1) - win + 1 # 配列１の長さ
    len2 = len(seq2) - win + 1 # 配列２の長さ

    width = 500 # 実際に描く幅
    height = 500 # 実際に描く高さ

    image = np.zeros( (height, width) ) # 実際に描く幅・高さの行列

    hash = {}
    for x in range(len1):
        sub1 = seq1[x:x+win]
        if sub1 not in hash:
            hash[sub1] = []
        hash[sub1].append(x)

    for y in range(len2):
        sub2 = seq2[y:y+win]
        py = int(y / len2 * height) # y を画像位置 py に
        if sub2 in hash:
            for x in hash[sub2]:
                px = int(x / len1 * width) # x を画像位置 px に
                image[py, px] = 1 # [py, px]にドット

    plt.imshow(image, extent = (1, len1, len2, 1), cmap="Grays")
    # カラーマップを灰色濃淡
    #plt.show()

    st.pyplot(plt) # 書き加える ： Streamlit上にMatplotlibを表示

st.title("Dot matrix") # タイトル

# 配列ファイルのアップローダ
file1 = st.sidebar.file_uploader("Sequence file 1:")
file2 = st.sidebar.file_uploader("Sequence file 2:")

win = st.sidebar.slider("Window size:", 4, 100, 10) # スライダー

if file1 and file2: # 2つのファイルがアップロードされていれば
    with StringIO(file1.getvalue().decode("utf-8")) as f1,\
         StringIO(file2.getvalue().decode("utf-8")) as f2:
        dotmatrix(f1, f2, win) # 関数呼び出し
# GO アプリの実行方法

## 必要要件

- Python 3.7 以上 他サイトを参照してインストールしてください（例）https://prog-8.com/docs/python-env
- 必要な Python ライブラリは `requirements.txt` に記載されています。

## 事前準備

**1度実行すればその後は実行する必要ないです**

   ターミナルにて、以下をコピペ

   ```bash
   git clone https://github.com/PM2951/GO.git
   cd GO
   pip install -r requirements.txt
   cd ~
   ```

## 実行

**アプリを起動する**

   ターミナルにて以下のコマンドでアプリケーションを起動します。
   
   ```bash
   python ~/GO/GOgraph_app.py
   ```

   環境によっては"python"を"python3"と置き換えて実行してください。
   
# PantherGOからGene ontologyの結果を取得する

   - tair : https://v2.arabidopsis.org/tools/go_term_enrichment.jsp
   - PantherGOの結果から、以下のような表を取得してください。（→ export table）

| GO biological process complete                      | Arabidopsis thaliana - REFLIST (27475) | upload_1 (2435) | upload_1 (expected)| upload_1 (over/under) | upload_1 (fold Enrichment) | upload_1 (P-value) |
|-----------------------------------------------------|-----------------------------------------|------------------|----------------------|------------------------|----------------------------|---------------------|
| response to chitin (GO:0010200)                    | 23                                      | 13               | 2.04              | +                      | 6.38                       | 2.73E-05           |
| cellular response to hypoxia (GO:0071456)          | 237                                     | 119              | 21.00              | +                      | 5.67                       | 3.95E-58           |
| cellular response to decreased oxygen levels (GO:0036294) | 239                                     | 120              | 21.18              | +                      | 5.67                       | 1.22E-58           |


   - これを、アプリ上のテキストボックスに入力するとグラフが作成できます。

   - プロットをPNG画像（800 dpi, 背景透過）として保存できます。


# Streamlit アプリの実行方法

このリポジトリには、`streamlit_app.py` という Streamlit アプリケーションのスクリプトが含まれています。このアプリケーションをローカル環境で実行するための手順を以下に示します。

## 必要要件

- Python 3.7 以上
- 必要な Python ライブラリは `requirements.txt` に記載されています。

## 実行手順

1. **リポジトリをクローンする**

   リポジトリをローカル環境にクローンします。

   ```bash
   git clone https://github.com/PM2951/GO.git
   cd GO
   ```
   もしくは、zipファイルをダウンロードして解凍してください。

2. **仮想環境を作成して有効化する (任意)**

   仮想環境を作成することで、依存関係の競合を防ぐことができます。なくても実行可能です。

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows の場合: venv\Scripts\activate
   ```

3. **必要なライブラリをインストールする**

   必要な Python ライブラリをインストールします。

   ```bash
   pip install -r requirements.txt
   ```

4. **Streamlit アプリを実行する**

   以下のコマンドでアプリケーションを起動します。

   ```bash
   streamlit run GOgraph.py
   ```

   もしくは、
   
   ```bash
   streamlit run GO/GOgraph.py
   ```

   初めての場合はEmailを聞かれますが、Emailっぽい形式であればなんでも大丈夫です。

   例) example@example.com　など

   コマンドを実行すると、ローカルサーバーが起動します。表示される URL（通常は `http://localhost:8501`）をブラウザで開くことで、アプリケーションにアクセスできます。
   
6. **PantherGOからGene ontologyの結果を取得する**

   tair : https://v2.arabidopsis.org/tools/go_term_enrichment.jsp

   | GO biological process complete                      | Arabidopsis thaliana - REFLIST (27475) | upload_1 (2435) | upload_1 (expected) | upload_1 (over/under) | upload_1 (fold Enrichment) | upload_1 (P-value) |
|-----------------------------------------------------|-----------------------------------------|------------------|----------------------|------------------------|----------------------------|---------------------|
| response to chitin (GO:0010200)                    | 23                                      | 13               | 2.04                 | +                      | 6.38                       | 2.73E-05           |
| cellular response to hypoxia (GO:0071456)          | 237                                     | 119              | 21.00                | +                      | 5.67                       | 3.95E-58           |
| cellular response to decreased oxygen levels (GO:0036294) | 239                                     | 120              | 21.18                | +                      | 5.67                       | 1.22E-58           |
| cellular response to oxygen levels (GO:0071453)    | 240                                     | 120              | 21.27                | +                      | 5.64                       | 2.24E-58           |
| indole glucosinolate metabolic process (GO:0042343) | 20                                      | 10               | 1.77                 | +                      | 5.64                       |                     |


8. **アプリケーションの終了**

   ターミナル上で [control + c] を押し、終了させる。

## 注意事項

- `requirements.txt` に記載されている依存関係を適切にインストールできない場合、環境や Python のバージョンを確認してください。
- 問題が発生した場合は、エラーメッセージを確認し、必要に応じて `pip` や Streamlit のドキュメントを参照してください。

## ライセンス

このプロジェクトのライセンスに関する情報は `LICENSE` ファイルをご参照ください。


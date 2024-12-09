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
   

   
6. **アプリケーションにアクセスする**

   コマンドを実行すると、ローカルサーバーが起動します。表示される URL（通常は `http://localhost:8501`）をブラウザで開くことで、アプリケーションにアクセスできます。

7. **アプリケーションの終了**

   ターミナル上で[control + c]を押し、終了させる。

## 注意事項

- `requirements.txt` に記載されている依存関係を適切にインストールできない場合、環境や Python のバージョンを確認してください。
- 問題が発生した場合は、エラーメッセージを確認し、必要に応じて `pip` や Streamlit のドキュメントを参照してください。

## ライセンス

このプロジェクトのライセンスに関する情報は `LICENSE` ファイルをご参照ください。


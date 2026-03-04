# オープンデータ可視化ツール (data_viz_tool)

このプロジェクトは、オープンデータを取得し、適切なグラフで可視化するPythonツールです。
また、OpenAI API を利用して、データに関する質問をすることができます。

## インストール方法

### 1. リポジトリをクローン (GitHubを使用する場合)
```sh
git clone https://github.com/yourusername/data_viz_tool.git
cd data_viz_tool

pip install -r requirements.txt


---

### **3. 使い方**
```md
## 使い方

1. Python スクリプトを実行し、CSVのURLを入力する
```sh
python -m data_viz_tool

2. データのカラム（列）を選択し、適切なグラフを生成


---

### **4. 環境変数の設定（OpenAI APIキー）**
```md
## 環境変数の設定

このツールでは OpenAI API を使用します。  
API キーを環境変数に設定してください。

```sh
export OPENAI_API_KEY="your-api-key"  # macOS/Linux
set OPENAI_API_KEY="your-api-key"  # Windows


---

### **5. ライセンス**
```md
## ライセンス
MIT License

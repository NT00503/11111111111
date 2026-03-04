import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import requests
import openai
import os
from dotenv import load_dotenv  # .env を読み込むライブラリ

# .env ファイルの読み込み
load_dotenv()

# OpenAI APIキーを環境変数から取得
openai.api_key = os.getenv("OPENAI_API_KEY")

# 日本語フォントの設定
import matplotlib
matplotlib.rcParams['font.family'] = 'MS Gothic'  # Windowsの場合

def preprocess_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    指定された列を数値型に変換し、欠損値を削除します。
    """
    for col in columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df.dropna(subset=columns)

def suggest_graph_type(df: pd.DataFrame, selected_columns: list) -> str:
    """
    ChatGPTを利用して適切なグラフタイプを提案する関数。
    """
    summary = df[selected_columns].describe().to_string()
    prompt = f"以下のデータの概要に基づいて、どのグラフタイプが最適かを提案してください:\n{summary}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "あなたはデータ分析の専門家です。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        suggestion = response['choices'][0]['message']['content'].strip()
        return suggestion
    except openai.error.OpenAIError as e:
        print(f"OpenAI APIエラー: {e}")
        return "エラーが発生しました。標準的な散布図を使用します。"

def fetch_data_from_url(file_url, encoding=None):
    """
    指定されたURLからデータを取得し、データフレームとして返します。
    """
    file_response = requests.get(file_url)
    file_content = file_response.content

    if encoding is None:
        encoding = "utf-8-sig"

    try:
        data = pd.read_csv(BytesIO(file_content), encoding=encoding)
        data.columns = data.columns.str.replace(r'^\ufeff', '', regex=True)
    except UnicodeDecodeError:
        print(f"エンコーディング'{encoding}'で失敗。Shift_JISを試します。")
        data = pd.read_csv(BytesIO(file_content), encoding="shift_jis")
        data.columns = data.columns.str.replace(r'^\ufeff', '', regex=True)

    return data

def plot_2d(df: pd.DataFrame, x_col: int, y_col: int):
    """
    2Dグラフを描画する関数。
    """
    x_label = df.columns[x_col - 1]
    y_label = df.columns[y_col - 1]

    df[x_label] = pd.to_numeric(df[x_label], errors='coerce')
    df[y_label] = pd.to_numeric(df[y_label], errors='coerce')
    df = df.dropna(subset=[x_label, y_label])

    plt.figure(figsize=(10, 6))
    plt.plot(df[x_label], df[y_label], marker='o', linestyle='-', label=f"{y_label} vs {x_label}")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(f"2D Plot: {y_label} vs {x_label}")
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_3d(df: pd.DataFrame, x_col: int, y_col: int, z_col: int):
    """
    3Dグラフを描画する関数。
    """
    from mpl_toolkits.mplot3d import Axes3D

    x_label = df.columns[x_col - 1]
    y_label = df.columns[y_col - 1]
    z_label = df.columns[z_col - 1]

    df[x_label] = pd.to_numeric(df[x_label], errors='coerce')
    df[y_label] = pd.to_numeric(df[y_label], errors='coerce')
    df[z_label] = pd.to_numeric(df[z_label], errors='coerce')
    df = df.dropna(subset=[x_label, y_label, z_label])

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(df[x_label], df[y_label], df[z_label], c='blue', marker='o', label=f"{z_label} vs {x_label} and {y_label}")
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_zlabel(z_label)
    ax.set_title(f"3D Plot: {z_label} vs {x_label} and {y_label}")
    plt.legend()
    plt.show()

def ask_question_about_data(df: pd.DataFrame):
    """
    データについてOpenAI APIを使用して質問する関数。
    """
    while True:
        print("\nデータに基づいて質問してください。")
        question = input("質問: ").strip()

        if question:
            summary = df.describe().to_string()
            prompt = f"以下のデータの概要に基づいて質問に答えてください:\n{summary}\n質問: {question}"

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "あなたはデータ分析のアシスタントです。"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=300
                )
                answer = response['choices'][0]['message']['content'].strip()
                print(f"回答: {answer}")
            except openai.error.AuthenticationError:
                print("OpenAI APIの認証エラー: APIキーを確認してください。")
            except openai.error.OpenAIError as e:
                print(f"OpenAI APIのエラー: {e}")
            except Exception as e:
                print(f"質問処理中にエラーが発生しました: {e}")

        print("\n質問を続けますか？")
        print("1. はい")
        print("2. いいえ")
        continue_question = input("番号を入力してください: ").strip()

        if continue_question == "2":
            print("質問を終了します。")
            break
        elif continue_question != "1":
            print("無効な入力です。質問を終了します。")
            break

def select_graph_type(dimension: str) -> str:
    """
    利用可能なグラフの種類を表示し、選択されたグラフの種類を返す。
    """
    print("\n利用可能なグラフの種類:")
    graph_types = {
        1: "散布図 (Scatter Plot)",
        2: "折れ線グラフ (Line Plot)",
        3: "縦棒グラフ (Vertical Bar Chart)",
        4: "横棒グラフ (Horizontal Bar Chart)",
        5: "円グラフ (Pie Chart)",
        6: "面グラフ (Area Chart)",
    }

    if dimension == "3d":
        graph_types[7] = "3D散布図 (3D Scatter Plot)"

    for key, value in graph_types.items():
        print(f"{key}. {value}")

    try:
        choice = int(input("\nグラフの種類を選択してください (番号): ").strip())
        return graph_types.get(choice, "不明なグラフタイプ")
    except ValueError:
        print("無効な入力です。数字を入力してください。")
        return "不明なグラフタイプ"

def interactive_plot_tool():
    """
    インタラクティブなプロットツールのメイン関数。
    """
    print("ようこそ！オープンデータ可視化ツールへ。\n")

    file_url = input("CSVファイルのURLを入力してください (例：https://〇〇〇/データ.csv): ").strip()

    df = fetch_data_from_url(file_url)
    if df.empty:
        print("データの読み込みに失敗しました。終了します。")
        return

    print("\n利用可能なデータ列:")
    for i, col in enumerate(df.columns, 1):
        print(f"{i}. {col}")

    selected_columns = input("\nグラフに使用する列番号をカンマ区切りで入力してください (例: 1,2): ").strip()
    selected_columns = [df.columns[int(idx) - 1] for idx in selected_columns.split(",")]

    # --- 前処理の適用 ---
    df = preprocess_columns(df, selected_columns)

    # --- ChatGPTによる提案 ---
    print("\nChatGPTに最適なグラフタイプを提案してもらいます...")
    suggested_graph_type = suggest_graph_type(df, selected_columns)
    print(f"提案されたグラフタイプ: {suggested_graph_type}")

    # 提案されたグラフタイプを使用するか確認
    print("\n提案されたグラフタイプを使用しますか？")
    print("1. はい")
    print("2. いいえ (手動で選択する)")

    choice = input("番号を入力してください: ").strip()
    if choice == "1":
        print(f"選択されたグラフタイプ: {suggested_graph_type}")
        graph_type = suggested_graph_type
    else:
        graph_type = select_graph_type("2d")  # 手動選択 (例: 2D)

    # グラフを描画
    if "3D" in graph_type:
        x_col = int(input("\nX軸に使用する列番号を入力してください: ").strip())
        y_col = int(input("Y軸に使用する列番号を入力してください: ").strip())
        z_col = int(input("Z軸に使用する列番号を入力してください: ").strip())
        plot_3d(df, x_col, y_col, z_col)
    else:
        x_col = int(input("\nX軸に使用する列番号を入力してください: ").strip())
        y_col = int(input("Y軸に使用する列番号を入力してください: ").strip())
        plot_2d(df, x_col, y_col)

    # --- 質問機能を呼び出す ---
    ask_question_about_data(df)

# --- 実行 ---
if __name__ == "__main__":
    interactive_plot_tool()
    
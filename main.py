# お題「文字お越しアプリ」
# TODO import 必要なライブラリ
# whisperの対応バージョンは3.8~11(2025/2/13時点)仮想環境必須
import whisper

# pip install --upgrade pip setuptools wheel
# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
# pip install -U openai-whisper


def main():
    print("文字お越しを開始します")

    # モデル指定
    # tinu < base < small < medium < turbo < large
    model = whisper.load_model("small", device="cpu")
    if model.device == "cuda":
        _ = model.half()
        _ = model.cuda()

    # TODO ファイル読み込み
    file: str = read_file()
    print(file)
    # TODO 文字お越し
    # TODO 辞書型として出力される
    result = output_result(model, file)

    # TODO テキストファイルに保存
    save_result(result)

    print("文字お越しが完了しました")


def read_file() -> str:
    file: str = (
        r"C:\Users\jyunya\Desktop\文字お越しPy\音声サンプル\サンプル会議音声.mp3"
    )
    return file


def output_result(model, file: str):
    result = model.transcribe(file, language="ja")
    return result


def save_result(result):
    # print(result["text"])
    with open("文字お越し出力.txt", "w", encoding="utf-8") as f:
        for row in result["text"]:
            # 型不一致を防ぐためにfp16をfp32に戻す
            if isinstance(row, whisper.model.LayerNorm):
                row.float()
            if row == "。" or row == "?" or row == "!":
                print(row, file=f)
            else:
                print(row, end="", file=f)


if __name__ == "__main__":
    main()

# お題「文字お越しアプリ」
# TODO import 必要なライブラリ
# whisperの対応バージョンは3.8~11(2025/2/13時点)仮想環境必須
# pip install --upgrade pip setuptools wheel
# pip install git+https://github.com/openai/whisper.git
import whisper

# pip install tqdm
import tqdm

# pip install pymediainfo
from pymediainfo import MediaInfo


def main():
    print("文字お越しを開始します\n")

    # モデル指定
    # tinu < base < small < medium < turbo < large
    model = whisper.load_model("small", device="cpu")
    # GPUのあるPCなら高速化可能
    if model.device == "cuda":
        _ = model.half()
        _ = model.cuda()

    file: str = read_file()

    duration: float = get_audio_duration(file)
    print(f"音声ファイルの長さ：{duration}ms")
    result: dict = output_result(model, file, duration)

    save_result(result)

    print("\n文字お越しが完了しました")


# 音声ファイル読み込み
def read_file() -> str:
    file: str = (
        r"C:\Users\jyunya\Desktop\文字お越しPy\音声サンプル\サンプル会議音声.mp3"
    )
    return file


# 音声ファイル読み込み
def output_result(model, file, duration) -> dict:
    with tqdm.tqdm(total=duration, desc="音声読み込み中") as pbar:
        result: dict = model.transcribe(file, verbose=True, language="ja")
        pbar.update(duration)
    return result


# テキストファイルに出力
def save_result(result):
    with open("文字お越し出力.txt", "w", encoding="utf-8") as f:
        for row in tqdm.tqdm(iterable=result["text"], desc="テキスト出力中"):
            # fp16をfp32に戻す
            if isinstance(row, whisper.model.LayerNorm):
                row.float()
            if row == "。" or row == "?" or row == "!":
                print(row, file=f)
            else:
                print(row, end="", file=f)


# 音声ファイルの長さを取得
def get_audio_duration(file) -> float:
    info = MediaInfo.parse(file)
    for track in info.tracks:
        return track.duration


if __name__ == "__main__":
    main()

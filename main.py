# お題「文字お越しアプリ」
# whisperの対応バージョンは3.8~11(2025/2/13時点)仮想環境必須
# pip install --upgrade pip setuptools wheel
# pip install git+https://github.com/openai/whisper.git
import whisper
import tkinter.filedialog

# pip install tqdm
import tqdm

# pip install pymediainfo
from pymediainfo import MediaInfo

import typing
import subprocess
import os
import tkinter


def main():
    print("文字お越しを開始します\n")
    try:
    # モデル指定
    # tinu < base < small < medium < turbo < large
    # TODO model_nameをユーザが選択できるように
        model_name: str = "small"
        model = whisper.load_model(name=model_name, device="cpu")
        if model.device == "cuda":
            """GPUのあるPCなら高速化可能"""
            _ = model.half()
            _ = model.cuda()

        file: str
        root_path: str
        file, root_path = read_file()

        duration: float = get_audio_duration(file)
        print(f"音声ファイルの長さ：{duration}ms")
        result: dict = output_result(model, file, duration)

        save_result(result)

        print("\n文字お越しが完了しました")
        subprocess.Popen(["explorer", root_path], shell=True)
    except:
        print("エラーによる終了")
        exit()

def read_file() -> typing.Tuple[str, str]:
    """音声ファイルを読み込む

    Returns:
        str,str: 音声ファイルの絶対パス,カレントディレクトリ
    """
    root = tkinter.Tk()
    root.withdraw()
    fileType = [("", "*.mp3"), ("", "*.wav")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    file: str = tkinter.filedialog.askopenfilename(filetypes=fileType, initialdir=iDir)
    return file, iDir


def output_result(model, file, duration) -> dict:
    """音声ファイルを読み込み、文字を返す

    Args:
        model (Whisper): whisperのload_model
        file (str): 音声ファイルの絶対パス
        duration (float): 音声ファイルの再生時間

    Returns:
        dict: 文字お越しデータ
    """
    with tqdm.tqdm(total=duration, desc="音声読み込み中") as pbar:
        result: dict = model.transcribe(file, verbose=True, language="ja")
        pbar.update(duration)
    return result


def save_result(result):
    """テキストファイルに出力

    :params result: 出力された文字データ
    :type result: dict

    """
    # TODO 出力ファイル名をユーザが指定できるように
    with open("文字お越し出力.txt", "w", encoding="utf-8") as f:
        for row in tqdm.tqdm(iterable=result["text"], desc="テキスト出力中"):
            # fp16をfp32に戻す
            if isinstance(row, whisper.model.LayerNorm):
                row.float()
            if row == "。" or row == "?" or row == "!":
                print(row, file=f)
            else:
                print(row, end="", file=f)


def get_audio_duration(file) -> float:
    """読み込んだ音声ファイルの再生時間を取得する<br>
    現状ほぼ無意味

    Args:
        file (str): 音声ファイルの絶対パス

    Returns:
        float: 音声ファイルの再生時間
    """
    info = MediaInfo.parse(file)
    for track in info.tracks:
        return track.duration


if __name__ == "__main__":
    main()

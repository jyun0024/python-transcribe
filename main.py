# お題「文字お越しアプリ」
# whisperの対応バージョンは3.8~11(2025/2/13時点)仮想環境必須
# pip install --upgrade pip setuptools wheel
# pip install git+https://github.com/openai/whisper.git
import whisper

# pip install flet
import flet

# pip install tqdm
import tqdm

# pip install pymediainfo
from pymediainfo import MediaInfo

import typing
import subprocess
import os

# ファイル選択をGUI化するために使用
import tkinter
import tkinter.filedialog


def main(page: flet.Page):

    page.title = "文字起こしアプリ"
    page.window.width = 500
    page.window.height = 600
    page.window.center()

    def click_submit(e):
        if radio_list.value is None and input_filename.value == "":
            t.value = "精度を選択し、出力ファイル名を入力してください"
            t.update()
        elif radio_list.value is None:
            t.value = "精度が選択されていません"
            t.update()
        elif input_filename.value == "":
            t.value = "出力ファイル名が入力されていません"
            t.update()
        else:
            # t.value = f"{radio_list.value}\n{input_filename.value}"
            t.value = "文字お越しを開始します"
            t.update()
            print(radio_list.value)
            print(input_filename.value)
            tr = Transcribe(model_name="small", output_filename="test")
            tr.transcribe_main()
            t.value = "文字お越しが完了しました"
            t.update()

    radio_guide_text = flet.Text("精度:必要メモリ")
    radio_list = flet.RadioGroup(
        content=flet.Column(
            [
                flet.Radio(value="tiny", label="tiny:1GB"),
                flet.Radio(value="base", label="base:1GB"),
                flet.Radio(value="small", label="small:2GB"),
                flet.Radio(value="medium", label="medium:5GB"),
                flet.Radio(value="large", label="large:10GB"),
                flet.Radio(value="turbo", label="turbo:6GB"),
            ]
        )
    )

    t = flet.Text()

    input_filename = flet.TextField(label="出力ファイル名を入力してください")
    page.add(
        radio_guide_text,
        radio_list,
        input_filename,
        flet.ElevatedButton("Submit", on_click=click_submit),
        t,
    )


class Transcribe:
    """文字起こしを行うクラス"""

    def __init__(self, model_name, output_filename):
        self.select_file: str = ""
        self.root = tkinter.Tk()
        self.root_path: str = os.path.abspath(os.path.dirname(__file__))
        self.model_name: str = model_name
        self.output_filename: str = output_filename

    def transcribe_main(self):
        # モデル指定
        # tiny < base < small < medium < turbo < large
        self.model = whisper.load_model(name=self.model_name)
        print(f"device:{self.model.device}")
        if self.model.device == "cuda":
            # GPUのあるPCなら高速化可能
            _ = self.model.half()
            _ = self.model.cuda()

        # ファイル取り込み、文字お越し
        self.read_file()
        duration: float = self.get_audio_duration()
        print(f"音声ファイルの長さ：{duration}ms")
        result: dict = self.output_result(duration)

        # アウトプット
        self.save_result(result)
        subprocess.Popen(["explorer", self.root_path], shell=True)

    # ファイルを開く
    def read_file(self):
        """音声ファイルを読み込む

        Returns:
            [str,str]: [音声ファイルの絶対パス , カレントディレクトリ]
        """
        self.root.withdraw()
        fileType = [("", "*.mp3"), ("", "*.wav")]
        # iDir = os.path.abspath(os.path.dirname(__file__))
        try:
            self.select_file = tkinter.filedialog.askopenfilename(
                filetypes=fileType, initialdir=self.root_path
            )
        except FileNotFoundError as e:
            print("ファイルが見つかりません")
            print(f"{e.__class__.__name__}: {e}")
            exit()

    def output_result(self, duration) -> dict:
        """音声ファイルを読み込み、文字を返す

        Args:
            model (Whisper): whisperのload_model
            select_file (str): 音声ファイルの絶対パス
            duration (float): 音声ファイルの再生時間

        Returns:
            dict: 文字お越しデータ
        """
        with tqdm.tqdm(total=duration, desc="音声読み込み中") as pbar:
            result: dict = self.model.transcribe(
                self.select_file, verbose=True, language="ja"
            )
            pbar.update(duration)
        return result

    def save_result(self, result):
        """テキストファイルに出力

        :params result: 出力された文字データ
        :type result: dict
        """
        # TODO 出力ファイル名をユーザが指定できるように
        with open(f"{self.output_filename}.txt", "w", encoding="utf-8") as f:
            for row in tqdm.tqdm(iterable=result["text"], desc="テキスト出力中"):
                # fp16をfp32に戻す
                if isinstance(row, whisper.model.LayerNorm):
                    row.float()
                if row == "。" or row == "?" or row == "!":
                    print(row, file=f)
                else:
                    print(row, end="", file=f)

    def get_audio_duration(self) -> float:
        """読み込んだ音声ファイルの再生時間を取得する<br>
        現状ほぼ無意味
        将来的に待機時間の推測に使用する

        Args:
            file (str): 音声ファイルの絶対パス

        Returns:
            float: 音声ファイルの再生時間
        """
        info = MediaInfo.parse(self.select_file)
        for track in info.tracks:
            return track.duration


if __name__ == "__main__":
    flet.app(main)
    # main()

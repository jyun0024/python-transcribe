# whisperの対応バージョンは3.8~11(2025/2/13時点)仮想環境必須
# pip install --upgrade pip setuptools wheel
# pip install git+https://github.com/openai/whisper.git
import whisper

# pip install pymediainfo
from pymediainfo import MediaInfo


class Transcribe:
    """文字起こしを行うクラス"""

    def __init__(self, model_name, output_filename, select_path):
        self.select_path: str = select_path
        # self.root = tkinter.Tk()
        # self.root_path: str = os.path.abspath(os.path.dirname(__file__))
        self.model_name: str = model_name
        self.output_filename: str = output_filename

        self.model = whisper.load_model(name=self.model_name)
        # print(f"device:{self.model.device}")
        if self.model.device == "cuda":
            # GPUのあるPCなら高速化可能
            _ = self.model.half()
            _ = self.model.cuda()

    # 開く
    # def read_file(self):
    #     """音声ファイルを読み込む

    #     Returns:
    #         [str,str]: [音声ファイルの絶対パス , カレントディレクトリ]
    #     """
    #     self.root.withdraw()
    #     fileType = [("", "*.mp3"), ("", "*.wav")]
    #     # iDir = os.path.abspath(os.path.dirname(__file__))
    #     try:
    #         self.select_file = tkinter.filedialog.askopenfilename(
    #             filetypes=fileType, initialdir=self.root_path
    #         )
    #     except FileNotFoundError as e:
    #         print("ファイルが見つかりません")
    #         print(f"{e.__class__.__name__}: {e}")
    #         exit()

    # 文字お越し
    def output_result(self) -> dict:
        """音声ファイルを読み込み、文字を返す

        Args:
            model (Whisper): whisperのload_model
            select_file (str): 音声ファイルの絶対パス

        Returns:
            dict: 文字お越しデータ
        """

        result: dict = self.model.transcribe(
            self.select_path, language="ja", verbose=True
        )

        return result

    # 出力
    def save_result(self, result):
        """テキストファイルに出力

        :params result: 出力された文字データ
        :type result: dict
        """
        # TODO 出力ファイル名をユーザが指定できるように
        with open(f"{self.output_filename}.txt", "w", encoding="utf-8") as f:
            for row in result["text"]:
                # fp16をfp32に戻す
                if isinstance(row, whisper.model.LayerNorm):
                    row.float()
                if row == "。" or row == "?" or row == "!":
                    print(row, file=f)
                else:
                    print(row, end="", file=f)

    def get_audio_duration(self) -> float:
        """読み込んだ音声ファイルの再生時間を取得する<br>
        将来的に待機時間の推測に使用する

        Args:
            file (str): 音声ファイルの絶対パス

        Returns:
            float: 音声ファイルの再生時間
        """
        print(self.select_path)
        info = MediaInfo.parse(self.select_path)
        for track in info.tracks:
            return track.duration

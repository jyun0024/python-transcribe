import flet
import subprocess
import os

# from subject import Subject
from transcribe import Transcribe

# from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

# text_subject = Subject()
# page_subject = Subject()


class FletApp:
    """fletアプリケーション"""

    def __init__(self, page: flet.Page):
        """コンストラクタ<br>
        ここで画面に初期表示させるコントローラを作成する

        Args:
            page (flet.Page): _description_
        """
        super().__init__()
        self.page = page
        self.page.title = "文字起こしアプリ"
        self.page.window.width = 500
        self.page.window.height = 600
        self.page.window.center()

        self.radio_table = flet.RadioGroup(
            flet.DataTable(
                columns=[
                    flet.DataColumn(flet.Text("選択")),
                    flet.DataColumn(flet.Text("精度")),
                    flet.DataColumn(flet.Text("必要メモリ")),
                    flet.DataColumn(flet.Text("読み込み速度")),
                ],
                rows=[
                    flet.DataRow(
                        cells=[
                            flet.DataCell(flet.Radio(value="tiny")),
                            flet.DataCell(flet.Text("tiny")),
                            flet.DataCell(flet.Text("～1GB")),
                            flet.DataCell(flet.Text("10倍")),
                        ],
                    ),
                    flet.DataRow(
                        cells=[
                            flet.DataCell(flet.Radio(value="base")),
                            flet.DataCell(flet.Text("base")),
                            flet.DataCell(flet.Text("～1GB")),
                            flet.DataCell(flet.Text("7倍")),
                        ],
                    ),
                    flet.DataRow(
                        cells=[
                            flet.DataCell(flet.Radio(value="small")),
                            flet.DataCell(flet.Text("small")),
                            flet.DataCell(flet.Text("～2GB")),
                            flet.DataCell(flet.Text("4倍")),
                        ],
                    ),
                    flet.DataRow(
                        cells=[
                            flet.DataCell(flet.Radio(value="medium")),
                            flet.DataCell(flet.Text("medium")),
                            flet.DataCell(flet.Text("～5GB")),
                            flet.DataCell(flet.Text("2倍")),
                        ],
                    ),
                    flet.DataRow(
                        cells=[
                            flet.DataCell(flet.Radio(value="large")),
                            flet.DataCell(flet.Text("large")),
                            flet.DataCell(flet.Text("～10GB")),
                            flet.DataCell(flet.Text("1倍")),
                        ],
                    ),
                    flet.DataRow(
                        cells=[
                            flet.DataCell(flet.Radio(value="rurbo")),
                            flet.DataCell(flet.Text("turbo")),
                            flet.DataCell(flet.Text("～6GB")),
                            flet.DataCell(flet.Text("8倍")),
                        ],
                    ),
                ],
            )
        )

        self.text = flet.Text()
        self.need_time = flet.Text()
        self.text_row = flet.Row(
            [
                self.text,
                self.need_time,
            ],
            wrap=True,
        )
        self.pick_file_dialog = flet.FilePicker(on_result=self.pick_file_result)
        self.page.overlay.append(self.pick_file_dialog)
        self.select_file_button = flet.FilledTonalButton(
            "ファイルを選択", on_click=lambda _: self.pick_file_dialog.pick_files()
        )
        self.selected_file = flet.Text()
        self.selected_path = flet.Text()
        self.selected_file_row = flet.Row(
            [
                self.select_file_button,
                self.selected_file,
            ],
            wrap=True,
        )

        self.input_filename = flet.TextField(label="出力ファイル名を入力してください")
        self.submit_button = flet.FilledButton("実行", on_click=self.click_submit)

        self.page.add(self.radio_table)
        self.page.add(self.selected_file_row)
        self.page.add(self.selected_path)
        self.page.add(self.input_filename)
        self.page.add(self.submit_button)
        self.page.add(self.text_row)

    def pick_file_result(self, e: flet.FilePickerResultEvent):
        """選んだファイルを表示する

        Args:
            e (flet.FilePickerResultEvent): _description_
        """
        self.selected_file.value = e.files[0].name
        self.selected_path.value = e.files[0].path
        print("selected_file:", self.selected_file)
        print("selected_path:", self.selected_path)
        print("e.files:", e.files)
        self.selected_file.update()
        self.selected_path.update()

    def get_speed(self, key):
        mapping = {
            "tiny": 10,
            "base": 7,
            "small": 4,
            "medium": 2,
            "large": 1,
            "turbo": 8,
        }
        return mapping.get(key)

    def all_control_disabled(self, bool: bool):
        """全てのコントロールの活性状態を変更する

        Args:
            bool (bool): True->非活性 <br> False->活性
        """
        for control in self.page.controls:
            control.disabled = bool
            self.page.update()

    def click_submit(self, e):
        """実行ボタンを押した時の処理

        Args:
            e (_type_): _description_

        Returns:
            _type_: _description_
        """

        if self.radio_table.value is None:
            self.text.value = "精度が選択されていません"
            self.text.update()
            return

        # ファイル選択
        self.page.add(self.pick_file_dialog, self.selected_file)

        if self.selected_file.value is None:
            self.text.value = "ファイルが選択されていません"
            self.text.update()
            return

        if self.input_filename.value == "":
            self.input_filename.value = (
                f"文字起こし_{self.selected_file.value.split('.')[0]}"
            )

        # t.value = f"{radio_table.value}\n{input_filename.value}"
        # TODO submitボタンの非活性化
        self.text.value = "文字お越しを開始します"
        self.text.update()
        self.all_control_disabled(True)
        # submit_button.disabled = True
        # submit_button.update()
        print(self.radio_table.value)
        print(self.input_filename.value)

        tr = Transcribe(
            model_name=self.radio_table.value,
            output_filename=self.input_filename.value,
            select_path=self.selected_path.value,
        )

        root = os.getcwd()

        # TODO プログレスバーの実装 終了推定時間の表示
        duration: float = tr.get_audio_duration()

        duration = duration / 1000
        print(f"音声ファイルの長さ：{duration}秒")
        duration = int(duration / self.get_speed(self.radio_table.value))
        print(f"所要時間：{duration}秒")
        self.need_time.value = f"推定所要時間：{duration}秒"
        self.need_time.update()

        # pb = flet.ProgressBar()
        # parsent_t = flet.Text()
        # finish_time = flet.Text(f"終了予測:{duration}秒")
        # progres_text = flet.Row(spacing=10, controls=[parsent_t, finish_time])
        # page.add(progres_text, pb)

        # def progress_bar():
        #     for i in range(0, int(duration) + 1):
        #         pb.value = i / duration
        #         parsent_t.value = f"{int(pb.value * 100)}%"
        #         time.sleep(1)
        #         parsent_t.update()
        #         pb.update()

        # TODO 並列処理の実装 プログレスバーとTranscribeの並列
        # with ThreadPoolExecutor(max_workers=2) as executor:
        #     executor.submit(progress_bar)
        #     # 文字お越し
        #     future = executor.submit(tr.output_result,duration)

        # TODO 平行処理の実装 プログレスバーとTranscribeの平行
        # with ProcessPoolExecutor(max_workers=2) as executor:
        #     executor.submit(progress_bar)
        #     # 文字お越し
        #     future = executor.submit(tr.output_result, duration)

        # 文字お越し
        result = tr.output_result()
        # アウトプット
        # result = future.result()
        # print(result)
        tr.save_result(result)
        # TODO submitボタンの活性化
        subprocess.Popen(["explorer", root], shell=True)
        # os.startfile(root)
        self.all_control_disabled(False)
        self.text.value = "文字お越しが完了しました"
        self.text.update()
        # submit_button.disabled = False
        # submit_button.update()
        print("ファイル出力終了")

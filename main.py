# お題「文字お越しアプリ」

# pip install flet
import flet

import typing
import subprocess
import os
import time

from subject import Subject
from transcribe import Transcribe

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def main(page: flet.Page):

    def pick_file_result(e: flet.FilePickerResultEvent):
        """選んだファイルを表示する

        Args:
            e (flet.FilePickerResultEvent): _description_
        """
        selected_file.value = e.files[0].name
        selected_path.value = e.files[0].path
        print("selected_file:", selected_file)
        print("selected_path:", selected_path)
        print("e.files:", e.files)
        selected_file.update()
        selected_path.update()

    def get_speed(key):
        mapping = {
            "tiny": 10,
            "base": 7,
            "small": 4,
            "medium": 2,
            "large": 1,
            "turbo": 8,
        }
        return mapping.get(key)

    def click_submit(e):
        """

        Args:
            e (_type_): _description_

        Returns:
            _type_: _description_
        """
        if radio_table.value is None and input_filename.value == "":
            text.value = "精度を選択し、出力ファイル名を入力してください"
            text.update()
        elif radio_table.value is None:
            text.value = "精度が選択されていません"
            text.update()
        elif input_filename.value == "":
            text.value = "出力ファイル名が入力されていません"
            text.update()
        else:
            # t.value = f"{radio_table.value}\n{input_filename.value}"
            # TODO submitボタンの非活性化
            text.value = "文字お越しを開始します"
            text.update()
            for control in page.controls:
                control.disabled = True
                page.update()
            # submit_button.disabled = True
            # submit_button.update()
            print(radio_table.value)
            print(input_filename.value)

            tr = Transcribe(
                model_name=radio_table.value,
                output_filename=input_filename.value,
                select_path=selected_path.value,
            )
            # ファイルを開く
            # tr.read_file()

            page.add(pick_file_dialog, selected_file)
            root = os.getcwd()

            # TODO プログレスバーの実装 終了推定時間の表示
            duration: float = tr.get_audio_duration()

            duration = duration / 1000
            print(f"音声ファイルの長さ：{duration}秒")
            duration = int(duration / get_speed(radio_table.value))
            print(f"所要時間：{duration}秒")
            need_time.value = f"推定所要時間：{duration}秒"
            need_time.update()

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
            for control in page.controls:
                control.disabled = False
                page.update()
            text.value = "文字お越しが完了しました"
            text.update()
            # submit_button.disabled = False
            # submit_button.update()
            print("ファイル出力終了")

    page.title = "文字起こしアプリ"
    page.window.width = 500
    page.window.height = 600
    page.window.center()

    # TODO テーブル形式で見やすくする
    radio_table = flet.RadioGroup(
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

    text = flet.Text()
    need_time = flet.Text()
    text_row = flet.Row(
        [
            text,
            need_time,
        ],
        wrap=True,
    )
    pick_file_dialog = flet.FilePicker(on_result=pick_file_result)
    page.overlay.append(pick_file_dialog)
    select_file_button = flet.FilledTonalButton(
        "ファイルを選択", on_click=lambda _: pick_file_dialog.pick_files()
    )
    selected_file = flet.Text()
    selected_path = flet.Text()
    selected_file_row = flet.Row(
        [
            select_file_button,
            selected_file,
        ],
        wrap=True,
    )

    input_filename = flet.TextField(label="出力ファイル名を入力してください")
    submit_button = flet.FilledButton("実行", on_click=click_submit)

    page.add(radio_table)
    page.add(selected_file_row)
    page.add(selected_path)
    page.add(input_filename)
    page.add(submit_button)
    page.add(text_row)


if __name__ == "__main__":
    flet.app(main)

from typing import TypeVar, Optional, Generic
import flet

T = TypeVar("T")


class Observer():
    """オブザーバークラス<br>
    変更されたvalueを受け取り、更新処理をする
    """

    def __init__(self, control):
        self.flet_control = control

    def update(self, observer: Optional[T]):
        """変更時に呼ばれるflet.update()

        Args:
            new_value (_type_): _description_
        """
        if self.flet_control.value != observer.value:
            self.flet_control.value = observer
            self.flet_control.update()

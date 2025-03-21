from typing import TypeVar, Optional, Generic
from observer import Observer

T = TypeVar("T")


class Subject(Generic[T]):
    """状態管理クラス<br>
        1.監視対象をbind()で登録する<br>
        2.set_value()でした場合、値が前回と異なる場合、observer.update()を呼ぶ
    """

    def __init__(self):
        self._value: Optional[T] = None
        self._observer_list: list[callable] = []
        
    def bind(self,observer):
        self._observer_list.append(observer)

    def set_value(self, new_value: Optional[T]):
        """変更を通知"""
        self._value = new_value
        self.notify()

    def notify(self):
        """オブザーバーに通知"""
        for observer in self._observer_list:
            observer.update(self._value)

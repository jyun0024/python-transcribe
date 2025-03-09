from typing import TypeVar, Optional, Generic
from observer import Observer

T = TypeVar("T")

class Subject(Generic[T]):
    """状態管理クラス"""

    def __init__(self,value: Optional[T]):
        """引数ありコンストラクタ

        Args:
            value (Optional[T]): インスタンス生成時の値
        """
        self._value: Optional[T] = value
        self._observer_list: list[callable] = []
        

    def attach(self, observer: callable):
        """オブザーバーを登録"""
        self._observer_list.append(observer)

    def detach(self, observer: callable):
        """オブザーバーを削除"""
        self._observer_list.remove(observer)

    def set_value(self, new_value: Optional[T]):
        """変更を通知"""
        self._value = new_value
        self.notify()

    def notify(self):
        """オブザーバーに通知"""
        for observer in self._observer_list:
            Observer.update(self._value)

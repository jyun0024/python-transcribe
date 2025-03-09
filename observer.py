class Observer:
    """オブザーバークラス<br>
    変化通知先
    """

    def __init__(self, control):
        self.flet_control = control

    def update(self, new_value):
        self.flet_control.value = new_value
        self.flet_control.update()

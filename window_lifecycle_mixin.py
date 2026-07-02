class WindowLifecycleMixin:
    def showEvent(self, e):
        super().showEvent(e)
        self._update_keep_on_top()

    def hideEvent(self, e):
        super().hideEvent(e)
        self._update_keep_on_top()

    def moveEvent(self, e):
        super().moveEvent(e)
        self._update_keep_on_top()
from PyQt5 import QtCore

class ZMQListener(QtCore.QObject):

    request = QtCore.pyqtSignal(dict)

    def __init__(self, parent):

        super(ZMQListener, self).__init__()
        self.parent = parent

    def loop(self):

        while self.parent.running:
            request = self.parent.socket.recv_json()
            self.request.emit(request)

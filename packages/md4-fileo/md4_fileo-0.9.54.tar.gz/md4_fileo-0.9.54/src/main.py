import sys

from loguru import logger
from pathlib import Path

from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import QApplication, QWidget

from .core import utils, app_globals as ag, iman
from .core.sho import shoWindow

if sys.platform.startswith("win"):
    from .core import win_win as win_activate
elif sys.platform.startswith("linux"):
    from .core import linux_win as win_activate
else:
    raise ImportError(f"doesn't support {sys.platform} system")


app: QApplication = None

@pyqtSlot(QWidget, QWidget)
def tab_pressed():
    global app
    old = app.focusWidget()
    if old is ag.dir_list:
        ag.file_list.setFocus()
    else:
        ag.dir_list.setFocus()

def set_logger(file):
    logger.remove()
    fmt = "{time:%b-%d %H:%M:%S} | {module}.{function}({line}): {message}"

    if file == "sys.stderr":
        logger.add(sys.stderr, format=fmt)
    else:
        logger.add(file, format=fmt)
    logger.info("START ==============================>")
    logger.info(f'{ag.app_name()=}, {ag.app_version()=}')

def instance_control(db_name: str):
    pid = iman.new_app_instance()

    ag.single_instance = utils.get_app_setting("SINGLE_INSTANCE", False)
    if pid:
        if ag.single_instance:
            win_activate.activate(pid)
            iman.app_instance_closed()

            sys.exit(0)
        else:
            ag.db.conn = None
            ag.db.path = db_name
            ag.db.restore = bool(db_name)
            logger.info(f'ag.DB: {ag.db!r}')


def start_app():
    global app
    app = QApplication([])

    try:
        thema_name = "default"
        log_qss = utils.get_app_setting("LOG_QSS", False)
        utils.apply_style(app, thema_name, to_save=log_qss)
    except KeyError as e:
        # message for developers
        logger.info(f"KeyError: {e.args}; >>> check you qss parameters file {thema_name}.param")
        return

    main_window = shoWindow()

    main_window.show()
    tab = QShortcut(QKeySequence(Qt.Key.Key_Tab), ag.app)
    tab.activated.connect(tab_pressed)

    sys.exit(app.exec())



def main(entry_point: str, db_name: str):
    # from datetime import datetime as dt
    # file_name = f"fill-{dt.now():%b-%d-%H}.log"
    # file_name = "sys.stderr"
    # set_logger(file_name)
    logger.info(entry_point)
    tmp = Path(entry_point)
    if getattr(sys, "frozen", False):

        ag.entry_point = (tmp.parent / 'fileo.exe').as_posix()
    else:
        ag.entry_point = tmp.name

    # utils.save_to_file("entry-point.txt", ag.entry_point)

    instance_control(db_name)

    start_app()

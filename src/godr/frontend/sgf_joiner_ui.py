import os
import sys

import pkg_resources
from PyQt5 import QtWidgets, QtCore
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QApplication, QMessageBox

from godr.sgf_joiner import SGFJoiner
from pathvalidate import ValidationError, validate_filename


class MergeSgfDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load Qt Designer form
        form_class, _ = uic.loadUiType(pkg_resources.resource_stream('godr.frontend.ui', "merge_sgf.ui"))
        form_class().setupUi(self)

        self.setWindowFlags(self.windowFlags() & (~QtCore.Qt.WindowContextHelpButtonHint))

        self.files = []
        self.outdir = None
        self.line_files = self.findChild(QtWidgets.QLineEdit, 'selected_files')
        self.line_outdir = self.findChild(QtWidgets.QLineEdit, 'selected_outdir')
        self.result_name_prefix = self.findChild(QtWidgets.QLineEdit, "select_result_name")
        self.status = self.findChild(QtWidgets.QLabel, 'status')

    def select_files(self):
        type_filter = "SGF (*.sgf)"
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFiles)
        names, _ = dialog.getOpenFileNames(self, caption="Выберите SGF", filter=type_filter)

        self.files = names
        file_names = [os.path.basename(name) for name in names]
        self.line_files.setText(str(file_names).translate({39: None})[1:-1])
        if names:
            self.outdir = os.path.dirname(names[0])
            self.line_outdir.setText(self.outdir)
            self.result_name_prefix.setText("joined_" + os.path.basename(self.files[0])[:-4])

    def select_outdir(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        start_dir = self.outdir if self.outdir else os.getcwd()
        self.outdir = dialog.getExistingDirectory(self, directory=start_dir)
        self.line_outdir.setText(self.outdir)

    def merge(self):
        if len(self.files) < 2:
            self.show_message("Выберите не менее 2 файлов")
            return

        if not self.outdir:
            self.show_message("Выберите выходную папку")
            return

        result_name_prefix_text = self.result_name_prefix.text()
        try:
            validate_filename(result_name_prefix_text)
        except ValidationError as e:
            self.show_message("Выберите корректное имя файла")
            return

        joiner = SGFJoiner()
        joiner.join_files(self.files)
        result = joiner.serialise()

        def get_result_filename(size):
            if len(result.items()) == 1:
                return "{}.sgf".format(result_name_prefix_text)
            return "{}_{}x{}.sgf".format(result_name_prefix_text, size, size)

        # check if sgf with selected name already exists
        for s, c in result.items():
            result_name = get_result_filename(s)
            if os.path.exists(os.path.join(self.outdir, result_name)):
                text = "Файл {} уже существует. Хотите его перезаписать?".format(result_name)
                dlg = QMessageBox(QMessageBox.Warning, "Файл уже существует",
                                  text, QMessageBox.Yes | QMessageBox.No)
                dlg.button(QMessageBox.Yes).setText("Да")
                dlg.button(QMessageBox.No).setText("Нет, выбрать другое имя файла")
                ret = dlg.exec()

                if ret != QMessageBox.Yes:
                    self.show_message("Выберите уникальное имя файла")
                    return

        for s, c in result.items():
            result_name = get_result_filename(s)
            with open(os.path.join(self.outdir, result_name), "wb") as fh:
                fh.write(c)

        self.show_message("Готово. Записано {} SGF.".format(len(result)))

    def show_message(self, msg):
        self.status.setText(msg)


def main():
    app = QApplication(sys.argv)
    window = MergeSgfDialog()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

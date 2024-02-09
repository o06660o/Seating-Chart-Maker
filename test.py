import random, json

a = [i + 1 for i in range(50)]

b = [f"{i + 1:02d}" for i in range(50)]
for col in (0, 1, 3, 4, 6, 7, 9, 10, 2, 5, 8):
    print(col)
print(b)

"py -m nuitka --standalone --enable-plugin=pyside6 --show-memory --show-progress --windows-disable-console --output-dir=output --windows-icon-from-ico=assets/icons/MainWindow.jpg --run main.py MainWindow.py SettingsDialog.py DrawingDialog.py util.py"

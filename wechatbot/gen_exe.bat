rmdir /s /q build
rmdir /s /q dist

pyinstaller -F --icon="icons/comm.ico" main.py -n WechatBot

pause
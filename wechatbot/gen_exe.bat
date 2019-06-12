rmdir /s /q build
rmdir /s /q dist

pyinstaller -F --icon="icons/comm.ico" wechatbot.py -n WechatBot

pause
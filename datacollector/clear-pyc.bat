@echo off
for /r . %%a in (*.pyc) do (
   del /a /f "%%a"
   echo %%a
)
 
for /r . %%a in (__pycache__) do (
   rd /s /q "%%a"
   echo %%a
)
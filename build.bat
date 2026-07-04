@echo off
echo 正在安装依赖...
pip install -r requirements.txt
echo.
echo 正在打包...
pyinstaller build.spec
echo.
echo 打包完成！
echo 可执行文件位于 dist\WindowsFileOrganizer.exe
pause

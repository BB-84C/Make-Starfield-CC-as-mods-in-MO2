@echo off
setlocal
set SCRIPT_DIR=%~dp0

:: 直接使用所有参数作为路径（保留空格）
python "%SCRIPT_DIR%make_mods_from_cc.py" %*

pause

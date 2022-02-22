@echo off

goto :PYTHON_CHECK

:PYTHON_CHECK
python -V | find /v "Python"    >NUL 2>NUL && (goto :FAIL)
python -V | find "Python"       >NUL 2>NUL && (goto :PASS)

:FAIL
echo Python is not installed or not on the path.
echo Please download python.
start "" "https://www.python.org/downloads/windows/"
goto :INSTALL_REQUIREMENTS

:PASS
goto :INSTALL_REQUIREMENTS

:INSTALL_REQUIREMENTS
pip install pillow
goto :RUN_PROGRAM

:RUN_PROGRAM
cd ..
python ./main.py

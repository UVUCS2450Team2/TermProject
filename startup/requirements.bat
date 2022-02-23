::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFB5YQA2NAE+1BaAR7ebv/NbGsU4VW+0zRKzoiODbcNwn71fpRYQi3H9ZjPcqHhRWajelajMVun1Hone5O8ibvDDyR0mF6gU5GGoU
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSTk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+JeA==
::cxY6rQJ7JhzQF1fEqQJQ
::ZQ05rAF9IBncCkqN+0xwdVs0
::ZQ05rAF9IAHYFVzEqQJQ
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQJQ
::dhA7uBVwLU+EWDk=
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATElA==
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCyDJGyX8VAjFB5YQA2NAE+1BaAR7ebv/NbGsU4VW+0zRKzoiODbcNwn71fpRYQi3H9ZjPcfGBpKage7Uio5uUpDoiqAL8L8
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
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
python ./main.py

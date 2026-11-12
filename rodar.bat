@echo off
setlocal
cd /d "%~dp0"

set "PY="
where py >nul 2>&1 && set "PY=py"
if not defined PY (
    where python >nul 2>&1 && set "PY=python"
)
if not defined PY (
    if exist "%USERPROFILE%\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe" (
        set "PY=%USERPROFILE%\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe"
    )
)

if not defined PY (
    echo.
    echo  Python nao encontrado nesta maquina.
    echo  Instale o Python 3.10 ou superior em https://python.org e rode de novo.
    echo.
    pause
    exit /b 1
)

%PY% -c "import openpyxl" >nul 2>&1
if errorlevel 1 (
    echo.
    echo  Falta a biblioteca openpyxl. Instalando...
    %PY% -m pip install --quiet openpyxl
    if errorlevel 1 (
        echo.
        echo  Nao foi possivel instalar. Rode manualmente:
        echo      %PY% -m pip install openpyxl
        echo.
        pause
        exit /b 1
    )
)

%PY% main.py %*
set "CODIGO=%ERRORLEVEL%"
if not "%CODIGO%"=="0" (
    echo.
    echo  A aplicacao terminou com codigo %CODIGO%.
    pause
)
endlocal

@echo off
chcp 65001 >nul
title Gerador de Relatorios Fiscais - RGF
cd /d "%~dp0"

echo ============================================================
echo   GERADOR DE RELATORIOS FISCAIS
echo ============================================================
echo.

echo Abrindo a interface grafica...
echo.
echo Se a janela nao abrir, use a linha de comando:
echo    python gerar_relatorios.py --entrada "C:\caminho\das\matrizes"
echo.

python gerar_relatorios.py --ui
if errorlevel 1 (
    echo.
    echo Nao foi possivel abrir a interface.
    pause
)

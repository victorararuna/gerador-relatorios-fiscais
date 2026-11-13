@echo off
chcp 65001 >nul
title Publicar no GitHub
cd /d "%~dp0"

echo ============================================================
echo   PUBLICAR O REPOSITORIO NO GITHUB
echo ============================================================
echo.

where git >nul 2>&1
if errorlevel 1 (
    echo Git nao encontrado.
    echo.
    echo Instale em: https://git-scm.com/download/win
    echo Depois de instalar, feche e abra este atalho de novo.
    echo.
    pause
    exit /b 1
)

echo Repositorio: victorararuna/gerador-relatorios-fiscais
echo.
echo Antes de continuar, crie o repositorio VAZIO em:
echo    https://github.com/new
echo Nome: gerador-relatorios-fiscais
echo NAO marque README, gitignore nem licenca.
echo.
set "PADRAO=https://github.com/victorararuna/gerador-relatorios-fiscais.git"
set /p URL="URL [Enter para usar %PADRAO%]: "

if "%URL%"=="" set "URL=%PADRAO%"
echo.
echo Enviando para: %URL%

echo.
echo [1/5] Inicializando o repositorio...
if not exist ".git" git init

echo [2/5] Configurando a branch principal...
git branch -M main

echo [3/5] Adicionando os arquivos...
git add -A

echo [4/5] Criando o commit...
git -c user.name="victorararuna" -c user.email="victorararuna@users.noreply.github.com" commit -m "Gerador de relatorios fiscais RREO/RGF a partir da MSC"

if errorlevel 1 (
    echo Nenhuma alteracao para commitar ou commit ja existente.
)

echo [5/5] Enviando para o GitHub...
git remote remove origin >nul 2>&1
git remote add origin "%URL%"
git push -u origin main

if errorlevel 1 (
    echo.
    echo Falha no envio. Verifique:
    echo   - se o repositorio existe e esta vazio no GitHub
    echo   - se voce esta autenticado (git config --global user.email)
    echo.
) else (
    echo.
    echo Repositorio publicado com sucesso!
)

pause

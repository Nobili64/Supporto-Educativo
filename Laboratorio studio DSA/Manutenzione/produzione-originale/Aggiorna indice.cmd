@echo off
setlocal
title Aggiorna indice - Laboratorio studio DSA
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Manutenzione\aggiorna-indice.ps1"
set "DSA_INDEX_RESULT=%ERRORLEVEL%"
if not "%DSA_INDEX_RESULT%"=="0" (
  echo.
  echo Controlla il messaggio sopra, correggi Catalogo.ods e riprova.
) else (
  echo.
  echo Aggiornamento completato. Se l'indice e' aperto, aggiorna la pagina.
)
echo.
pause
exit /b %DSA_INDEX_RESULT%

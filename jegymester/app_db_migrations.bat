@echo off

if not exist "..\env" (
    echo A virtuális környezet nem található. Ellenőrizd az gydsm_jegymester alatt env néven van-e a virtuális környezet.
    exit /b 1
)

call ..\env\Scripts\activate


flask db migrate
flask db upgrade

echo Migráció sikeresen végrehajtva!
pause
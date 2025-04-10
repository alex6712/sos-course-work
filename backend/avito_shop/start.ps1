# tl;dr СКРИПТ НЕ РАБОТАЕТ
#
# При запуске сервера с помощью этого скрипта
# возникают проблемы с pydantic_settings.
#
# Ломается логика парсинга файла ".env".
#
# Поиск возможных путей исправления ни к чему
# не привёл.
#
# К сожалению, скрипт хоть и запускает сервер,
# но дальнейшая его работа невозможна по вышеописанной
# причине.

$OutputEncoding = [System.Text.Encoding]::UTF8
Invoke-Expression (poetry env activate)

$envPath = ".env"
Get-Content $envPath | ForEach-Object {
    if ($_ -match "^\s*([^#][^=]*)=(.*)$") {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()
        [System.Environment]::SetEnvironmentVariable($key, $value, "Process")
    }
}

$reloadFlag = ""
if ($env:DEV_MODE -eq "True") {
    $reloadFlag = "--reload"
}

uvicorn main:avito_shop --host $env:DOMAIN --port $env:BACKEND_PORT $reloadFlag

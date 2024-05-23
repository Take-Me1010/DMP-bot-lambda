Set-StrictMode -Version Latest

# Set default encoding to UTF-8
$OutputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['*:Encoding'] = 'utf8'

pipenv requirements > requirements.txt

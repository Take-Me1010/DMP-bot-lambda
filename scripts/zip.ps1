Remove-Item .\app\package\**\__pycache__ -Recurse -Force
Compress-Archive ./app/*.py -DestinationPath app.zip -Force

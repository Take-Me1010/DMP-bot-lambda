Remove-Item .\app\package\**\__pycache__ -Recurse -Force

Compress-Archive ./app/*.py -DestinationPath app.zip -Force
# Compress-Archive ./app/package/* -DestinationPath app.zip -Update -Force

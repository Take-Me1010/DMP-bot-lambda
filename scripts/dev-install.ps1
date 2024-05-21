
# dependecies for lambda function
$env:PIP_TARGET='app/package'

# pynacl は Layer に含めるためここでは app/package にインストールしない
# pipenv install pynacl

Remove-Item Env:\PIP_TARGET

# or simply use pip
# pip install --target ./app/package pynacl

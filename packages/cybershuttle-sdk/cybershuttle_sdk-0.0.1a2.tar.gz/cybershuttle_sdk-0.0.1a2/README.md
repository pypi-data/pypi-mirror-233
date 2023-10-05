pip3 install grpcio==1.47.0rc1
pip3 install grpcio-tools==1.47.0rc1



rm -rf dist
python3 -m pip install --upgrade build
python3 -m build
python3 -m pip install --upgrade twine
python3 -m twine upload --repository pypi dist/*
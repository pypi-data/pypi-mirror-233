Build & Deploy:

python setup.py sdist bdist_wheel
python -m pip install -e ./
twine upload dist/* --verbose -u __token__ -p pypi-xxx...
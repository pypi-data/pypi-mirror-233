rm dist/*
rm -r RobotsToolsData
python3 -m build
python3 -m twine upload -r pypi dist/* --verbose
echo "pip install -i https://pypi.org/simple/ RobotsTools==$(head -n 7 pyproject.toml | tail -n 1 | sed 's/.*"\([^"]*\)".*/\1/')"
echo "pip install -i https://pypi.org/simple/ RobotsTools==$(head -n 7 pyproject.toml | tail -n 1 | sed 's/.*"\([^"]*\)".*/\1/')" | sh
sleep 2
echo "pip install -i https://pypi.org/simple/ RobotsTools==$(head -n 7 pyproject.toml | tail -n 1 | sed 's/.*"\([^"]*\)".*/\1/')" | sh

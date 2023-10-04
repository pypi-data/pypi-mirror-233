cd ../..
rm -r tests/RobotsTools
cp -r src/RobotsTools tests/
echo "copied RobotsTools to tests/RobotsTools"
python3 tests/RobotsTools/__init__.py
#echo "ran python programs without problem"
python3 tests/testMain.py

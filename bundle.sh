rm -rf multitroids.app
python setup.py py2app
cp -rf Resources/* dist/game_manager.app/Contents/Resources
cp -rf dist/game_manager.app ./multitroids.app

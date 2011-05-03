rm -rf multitroids.app
python setup.py py2app
cp -rf dist/game_manager.app ./multitroids.app
cp raleway_thin.ttf multitroids.app/Contents/Resources

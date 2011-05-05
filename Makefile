app: $(wildcard *.py)
	rm -rf multitroids.app dist/multitroids.app
	python setup.py py2app
	mv -f dist/game_manager.app dist/multitroids.app
	cp -rf Resources/* dist/multitroids.app/Contents/Resources
	cp -rf dist/multitroids.app ./multitroids.app

dmg: app
	rm -f multitroids.dmg
	hdiutil create multitroids.dmg -srcfolder dist -volname multitroids

clean:
	rm -rf dist/* multitroids.app multitroids.dmg
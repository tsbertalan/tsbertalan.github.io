all:
	cp ../Job\ Search/Resume/resume_TomBertalan.pdf ./
	cd bin && export PYTHONPATH=$PYTHONPATH:`pwd`/../src/ && python createSiteFromDirs.py

view:
	google-chrome index.html

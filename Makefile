all: 
	cp ../Job\ Search/Resume/resume.pdf ./
	cd bin && export PYTHONPATH=$PYTHONPATH:`pwd`/../src/ && python createSiteFromDirs.py


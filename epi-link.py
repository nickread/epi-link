#!/usr/bin/python

import os
import re
import shutil
import sys

sourceBaseDir = '/Volumes/HOME MEDIA/Incoming'
destinationBaseDir = '/Volumes/HOME MEDIA/TV'
validExtensions = ['avi', 'mp4', 'm4v']

def showSpecificChanges(fn):

	# Some shows needs the year - 'V 2009' -> 'V (2009)'
	fn = re.sub(r'V 2009', 'V (2009)', fn)
	fn = re.sub(r'Doctor Who 2005', 'Doctor Who (2005)', fn)
	if not re.match(r'Merlin.+2008', fn):
		fn = re.sub(r'Merlin', 'Merlin (2008)', fn)

	# 'and' needs an ampersand in some cases
	fn = re.sub(r'Brothers And Sisters', 'Brothers & Sisters', fn)

	# Remove series names
	fn = re.sub(r' The Golden Mile', '', fn)

	return fn

def getShowSeasonEpisode(fn):
	# All examples are for Season 1, Episode 23

	# S01E23
	m = re.match(r'(?i)(.+)S(\d\d)E(\d\d)', fn)
	if m:
		return (m.group(1), int(m.group(2)), int(m.group(3)))
	
	# 1x23
	m = re.match(r'(.+)(\d)x(\d\d)', fn)
	if m:
		return (m.group(1), int(m.group(2)), int(m.group(3)))

	# 123
	# Careful to not match years by not matching a digit on either side of the triplet
	m = re.match(r'(.+[^\d])(\d)(\d\d)[^\d]', fn)
	if m:
		return (m.group(1), int(m.group(2)), int(m.group(3)))
	
	return (None, -1, -1)


# TODO: Expand RARs automatically before searching for episodes?  Maybe just print out a warning?
for srcDir, srcSubDirs, srcFns in os.walk(sourceBaseDir):

	# Don't traverse into directories that contains "Samples" of the real thing
	if 'Sample' in srcSubDirs:
		srcSubDirs.remove('Sample')
	
	for srcFn in srcFns:
		extension = re.search(r'\.([^\.]+)$', srcFn).group(1)
		if extension not in validExtensions:
			continue

		(showname, season, episode) = getShowSeasonEpisode(srcFn)
		if not showname:
			continue
			
		showname = re.sub(r'[-_\.]+', ' ', showname)
		showname = re.sub(r'(?i)repack', '', showname)
		showname = showname.strip()
		showname = showname.title()
		showname = re.sub(r' (\d\d\d\d)$', r' (\1)', showname)
		showname = showSpecificChanges(showname)
	
		destDir = '%s/Season %d' % (showname, season)
		destFn = '%s - S%02dE%02d.%s' % (showname, season, episode, extension)
		
		fullSrcFn = os.path.join(srcDir, srcFn)
		fullDestDir = os.path.join(destinationBaseDir, destDir)
		fullDestFn = os.path.join(fullDestDir, destFn)
		
		print fullDestFn

		if os.path.lexists(fullDestFn):
			sys.exit('The above file already exists - not moving %s until it is sorted out' % (srcFn))

		if not os.path.lexists(fullDestDir):
			os.makedirs(fullDestDir)

		shutil.move(fullSrcFn, fullDestFn)
		#shutil.copyfile(fullSrcFn, fullDestFn)



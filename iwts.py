#!/bin/python3


import subprocess
import sys
from os import path as ospath
from os import listdir
import os
import tempfile
import shutil
import stat

def cmd_to_stdout_str(cmd):
	return subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')

#def get_folder(line):
#	i = line.find('/')
#	if i == -1:
#		return line
#	else:
#		return line[0:i]
#def zip_are_all_files_in_same_folder(fname):
#	files = cmd_to_stdout_str(['zip', '-sf', fname]).splitlines()
#	files.pop() # get rid of the "Total n files" line
#	files.pop(0) # get rid of the "Archive contains" line
#	if len(files) == 0:
#		return True
#	prefix = get_folder(files[0])
#	for f in files:
#		if get_folder(f) != prefix:
#			return False
#	return True

def mk_dir_get_path(fname):
	base = ospath.splitext(ospath.split(fname)[1])[0]
	foldername = base
	i = 2
	while ospath.exists(foldername):
		foldername = f'{base}-{i}'
		i += 1
	path = f'./{foldername}'
	subprocess.run(['mkdir', path])
	return path

def extract_zip(fname):
	path = mk_dir_get_path(fname)
	subprocess.run(['unzip', fname, '-d', path])
	maybe_flatten(path)

def extract_tar(fname):
	path = mk_dir_get_path(fname)
	subprocess.run(['tar', 'xf', fname, '-C', path, '--no-same-owner'])
	# mess with permissions, because --no-same-permissions is bad
	for p, dirs, files in os.walk(path):
		os.chmod(p, 0o755)
		for f in files:
			fpath = ospath.join(p, f)
			m = os.stat(fpath).st_mode
			xperms = m & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
			os.chmod(fpath, 0o644 | xperms)
	maybe_flatten(path)

# if the provided directory contains only one entry,
# and that entry is a directory,
# move everything out of the subdirectory and into the directory
def maybe_flatten(dir_path):
	l = listdir(dir_path)
	if len(l) != 1:
		return False
	subentry_path = ospath.join(dir_path, l[0])
	if not ospath.isdir(subentry_path):
		return False
	subdir_path = subentry_path
	# make tmp dir
	tmpdir_path = tempfile.mkdtemp()
	subtmpdir_path = ospath.join(tmpdir_path, "a")
	shutil.move(subdir_path, subtmpdir_path)
	# move the files
	entries = listdir(subtmpdir_path)
	for e in entries:
		oldepath = ospath.join(subtmpdir_path, e)
		newepath = ospath.join(dir_path, e)
		shutil.move(oldepath, newepath)
	# clean up tmp dir
	shutil.rmtree(tmpdir_path)
	return True


def extract(fname):
	# TODO: better file detection
	if fname.endswith('.zip') or fname.endswith('.epub') or fname.endswith('.htmlz'):
		extract_zip(fname)
	elif fname.endswith('.tar.gz') or fname.endswith('.tar.xz'):
		extract_tar(fname)
	else:
		print(f'file extension unknown')

if __name__ == "__main__":
	extract(sys.argv[1])

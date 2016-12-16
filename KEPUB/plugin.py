#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, absolute_import, print_function

import sys
import os
import tempfile, shutil
import re

try:
	from urllib.parse import unquote
except ImportError:
	from urllib import unquote

from epub_utils import epub_zip_up_book_contents

import tkinter
import tkinter.ttk as tkinter_ttk
import tkinter.constants as tkinter_constants
import tkinter.filedialog as tkinter_filedialog
from kepubify import Kepubify

_USER_HOME = os.path.expanduser("~")

def write_file(data, href, temp_dir, unquote_filename=False, in_oebps=True):
	"""
	Write data to temp_dir/OEBPS/href (if in_oebps is True),
	or to temp_dir/href (if in_oebps), passing href through unquote()
	if unquote_filename is True.
	:param data: the data to be written
	:type  data: str
	:param href: the (internal) path of the file
	:type  href: str
	:param temp_dir: the path to the temporary directory
	:type  temp_dir: str
	:param unquote_filename: if True, pass href through unquote()
	:type  unquote_filename: bool
	:param in_oebps: if True, href is into the subtree rooted at OEBPS/
	:type  in_oebps: bool
	"""
	if unquote_filename:
		destdir = ""
		filename = unquote(href)
		if "/" in href:
			destdir, filename = unquote(filename).split("/")
		fpath = os.path.join(temp_dir, "OEBPS", destdir, filename)
	else:
		if in_oebps:
			fpath = os.path.join(temp_dir, "OEBPS", href)
		else:
			fpath = os.path.join(temp_dir, href)
	with open(fpath, "wb") as file_obj:
		file_obj.write(data.encode("utf-8"))

# the plugin entry point
def run(bk):

	temp_dir = tempfile.mkdtemp()

	# copy all files to a temporary destination folder
	# to get all fonts, css, images, and etc
	bk.copy_book_contents_to(temp_dir)

	kepubify = Kepubify()

	# parse all xhtml/html files
	for mid, href in bk.text_iter():
		print("..converting: ", href, " with manifest id: ", mid)
		#data, mprops, sprops, etypes = convert_xhtml(bk, mid, href)

		data = kepubify.add_kobo_spans(bk.readfile(mid))

		# write out modified file
		write_file(data, href, temp_dir, unquote_filename=True)


	# finally ready to build epub
	print("..creating: kepub")
	data = "application/epub+zip"
	write_file(data, "mimetype", temp_dir, in_oebps=False)

	# ask the user where he/she wants to store the new epub
	# TODO use dc:title from the OPF file instead
	doctitle = "filename"
	fname = cleanup_file_name(doctitle) + ".kepub.epub"
	localRoot = tkinter.Tk()
	localRoot.withdraw()
	fpath = tkinter_filedialog.asksaveasfilename(
		parent=localRoot,
		title="Save KEPUB As...",
		initialfile=fname,
		initialdir=_USER_HOME,
		defaultextension=".kepub.epub"
		)
	# localRoot.destroy()
	localRoot.quit()
	if not fpath:
		shutil.rmtree(temp_dir)
		print("KePub plugin cancelled by user")
		return 0

	epub_zip_up_book_contents(temp_dir, fpath)
	shutil.rmtree(temp_dir)

	print("Output Conversion Complete")
	# Setting the proper Return value is important.
	# 0 - means success
	# anything else means failure
	return 0

def cleanup_file_name(name):
	import string
	_filename_sanitize = re.compile(r'[\xae\0\\|\?\*<":>\+/]')
	substitute='_'
	one = ''.join(char for char in name if char in string.printable)
	one = _filename_sanitize.sub(substitute, one)
	one = re.sub(r'\s', '_', one).strip()
	one = re.sub(r'^\.+$', '_', one)
	one = one.replace('..', substitute)
	# Windows doesn't like path components that end with a period
	if one.endswith('.'):
		one = one[:-1]+substitute
	# Mac and Unix don't like file names that begin with a full stop
	if len(one) > 0 and one[0:1] == '.':
		one = substitute+one[1:]
	return one

def main():
	print("I reached main when I should not have\n")
	return -1

if __name__ == "__main__":
	sys.exit(main())

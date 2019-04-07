""" 
  Copyright (C) 2018 Claude SIMON (http://q37.info/contact/).

	This file is part of XDHq.

	XDHq is free software: you can redistribute it and/or
	modify it under the terms of the GNU Affero General Public License as
	published by the Free Software Foundation, either version 3 of the
	License, or (at your option) any later version.

	XDHq is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
	Affero General Public License for more details.

	You should have received a copy of the GNU Affero General Public License
	along with XDHq If not, see <http://www.gnu.org/licenses/>.
 """

import os, subprocess, sys

RT_VOID = 0
RT_STRING = 1
RT_STRINGS = 2

def isWin():
	return sys.platform == "win32"

def isDev():
	return "EPEIOS_SRC" in os.environ

def open(document):
	platform = sys.platform
	if platform == "win32":
		os.startfile(document)	# Exists only on Windows!
	else:
		if platform == "darwin":
			opener = "open"
		elif platform == "cygwin":
			opener = "cygstart"
		else:
			opener = "xdg-open"
		try:
			subprocess.call(opener + " " + document + " &", shell=True)
		except:
			pass

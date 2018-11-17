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

import XDHq
from threading import Thread
import threading

readAsset = XDHq.readAsset

def createXML(rootTag):
	return XDHq.XML(rootTag)

def worker(userObject,dom,callbacks):
	while True:
		[action,id] = dom.getAction()
		callbacks[action](userObject, dom, id )

def launch(newSessionAction, callbacks, new = lambda: None, headContent = "", dir = ""):
	XDHq.launch(newSessionAction,headContent,dir)

	while True:
		threading.Thread(target=worker, args=(new(), XDHq.DOM(), callbacks)).start()

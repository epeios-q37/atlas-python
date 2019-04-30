# *Python* version of the *Atlas* toolkit

**If you are looking for the *WebGPIO* application, you will find it at the bottom of this page (in the *Raspberry Pi*/*ODROID-C2* section).**

![For Python](http://q37.info/download/assets/Python.png "Python logo")

[![Version 0.9.4](https://img.shields.io/static/v1.svg?&color=90b4ed&label=Version&message=0.9.4)](http://q37.info/s/gei0veus)

A fast and easy way to add a graphical user interface ([GUI](http://q37.info/s/hw9n3pjs)) to your *Python* programs.

With the *Atlas* toolkit, you obtain hybrid programs. Like desktop applications, the same code can handle both [front and back ends](http://q37.info/s/px7hhztd), and, like web applications, the programs will be reachable from all over the internet.

If you want to use the *Atlas* toolkit without installing the examples, simply install the [*atlastk* package from *PyPI*](http://q37.info/s/9srmskcm) (`pip install atlastk`). This package has no dependencies.

You can also use the *Atlas* toolkit on [*Repl.it*](http://q37.info/s/mxmgq3qm), an [online IDE](http://q37.info/s/sssznrb4), so you have nothing to install. You will find some examples in the next sections.

*To support this project, please upvote this [pull request](https://github.com/vinta/awesome-python/pull/1272).*

## *15-puzzle* game

Before we dive into source code, let's begin with a live demonstration of the [*15-puzzle* game](http://q37.info/s/jn9zg3bn) made with *Atlas* toolkit: <http://q37.info/s/mdghbt3n> ([more about live demonstrations](http://q37.info/s/zgvcwv7j))!

## *Hello, World!*

Here's how a [*Hello, World!*](https://en.wikipedia.org/wiki/%22Hello,_World!%22_program) type program made with the *Atlas* toolkit looks like:

![Little demonstration](http://q37.info/download/assets/Hello.gif "A basic example")

- `git clone http://github.com/epeios-q37/atlas-python`
- `cd atlas-python`
- `python Hello/Hello.py`

You can also put below source code in a file and launch it after having installed the [*atlastk* package](http://q37.info/s/9srmskcm) (`pip install atlastk`), or, with absolutely no installation, paste the below code [here](http://q37.info/s/srnnb7hj), and open the displayed *URL* in a web browser.

For a live demonstration: <http://q37.info/s/vhnb3q3v>.

Source code:

```python
# Following two lines can be removed:
# - if the 'Atlas.python.zip' file is referenced in 'PYTHONPATH',
# - if you made a '[python -m] pip install [--user] atlastk',
# - if you paste this code in Repl.it.
import os, sys
sys.path.append("Atlas.python.zip") # Add the path to 'Atlas.python.zip' if needed.

import atlastk as Atlas

body = """
<div style="display: table; margin: 50px auto auto auto;">
 <fieldset>
  <input id="input" maxlength="20" placeholder="Enter a name here" type="text"
         data-xdh-onevent="Submit" value="World"/>
  <div style="display: flex; justify-content: space-around; margin: 5px auto auto auto;">
   <button data-xdh-onevent="Submit">Submit</button>
   <button data-xdh-onevent="Clear">Clear</button>
  </div>
 </fieldset>
</div>
"""

def acConnect(this, dom, id):
  dom.setLayout("", body)
  dom.focus("input")

def acSubmit(this, dom, id):
  dom.alert("Hello, " + dom.getContent("input") + "!")
  dom.focus("input")

def acClear(this, dom, id):
  if ( dom.confirm("Are you sure?") ):
    dom.setContent("input", "")
  dom.focus("input")

callbacks = {
  "": acConnect,  # This key is the action label for a new connection.
  "Submit": acSubmit,
  "Clear": acClear,
}
  
Atlas.launch(callbacks)
```

## *TodoMVC*

And here's how the *Atlas* toolkit version of the [*TodoMVC*](http://todomvc.com/) application looks like:

![TodoMVC](http://q37.info/download/TodoMVC.gif "The TodoMVC application made with the Atlas toolkit")

For a live demonstration: <http://q37.info/s/n9nnwzcg>.

## Content of the repository

The `atlastk` directory contains the *Python* source code of the *Atlas* toolkit, which is not needed to run the examples.

`Atlas.python.zip` is the file you have to reference in `PYTHONPATH` in order to use the *Atlas* toolkit in your own program (unless you have installed the [*atlastk* package](http://q37.info/s/9srmskcm) with `pip install atlastk`).

All other directories are examples.

To run an example, launch `python <Name>`, where `<Name>` is the name of the example (`Blank`, `Chatroom`…), except for the *ErgoJr*, *GPIO* and *RGB* applications, which are detailed just below.

The *Stars* application is an example where the *Atlas* *toolkit* is used to control a [*Pygame*](https://en.wikipedia.org/wiki/Pygame) based application. Of course, *Pygame* needs to be installed.

## *Raspberry Pi*/*ODROID-C2*

The *GPIO* and *RGB* applications are designed to be used on a *Raspberry Pi* or a *ODROID-C2*.

For the *Raspberry Pi*, the `RPi.GPIO` *Python* module have to be installed (this is probably already the case).

For the *ODROID-C2*, The *Python* version of *WiringPi* must be installed, and the application has to be launched with `sudo` (`sudo python GPIO` or `sudo python RGB`).

The *ErgoJr* application is experimental and to control a *Poppy* *Ergo Jr* robot.

The *RGB* application is dedicated to the control of a RGB led, and the *GPIO* (aka *WebGPIO*) application allows to control the basic pins. Here is a video to see how they works:

[![RGB video](https://img.youtube.com/vi/C4p2iX6gc-Q/0.jpg)](https://www.youtube.com/watch?v=C4p2iX6gc-Q)

Same video on [*PeerTube*](https://en.wikipedia.org/wiki/PeerTube) : <https://peertube.video/videos/watch/e7e02356-c9c3-4590-8ec0-8f8da06ff312>

This applications are only examples to show how easily it is to write your own applications.

## Miscellaneous

The *Atlas* toolkit is also available for:

- *Java*: <http://github.com/epeios-q37/atlas-java>
- *Node.js*: <http://github.com/epeios-q37/atlas-node>
- *PHP*: <http://github.com/epeios-q37/atlas-php>
- *Ruby*: <http://github.com/epeios-q37/atlas-ruby>

For more information about the *Atlas* toolkit, go to <http://atlastk.org/>.
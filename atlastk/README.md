# *Python* version of the *Atlas* toolkit

![For Python](https://q37.info/download/assets/Python.png "Python logo")

[![Run on Repl.it](https://repl.it/badge/github/epeios-q37/atlas-python)](https://q37.info/s/vwpsw73v)
[![Version 0.11](https://img.shields.io/static/v1.svg?&color=90b4ed&label=Version&message=0.11)](http://github.com/epeios-q37/atlas-node/)
[![Stars](https://img.shields.io/github/stars/epeios-q37/atlas-python.svg?style=social)](https://github.com/epeios-q37/atlas-python/stargazers)
[![license: MIT](https://img.shields.io/github/license/epeios-q37/atlas-python?color=yellow)](https://github.com/epeios-q37/atlas-python/blob/master/LICENSE)
[![Homepage](https://img.shields.io/static/v1?label=homepage&message=atlastk.org&color=ff69b4)](https://atlastk.org)

[![Version](https://img.shields.io/pypi/v/atlastk?style=for-the-badge&color=90b4ed&label=PyPi)![Download stats](https://img.shields.io/pypi/dm/atlastk.svg?style=for-the-badge)](http://q37.info/s/9srmskcm)


*NOTA*: this toolkit is also available for:

- *Java*: <http://github.com/epeios-q37/atlas-java>
- *Node.js*: <http://github.com/epeios-q37/atlas-node>
- *Perl*: <http://github.com/epeios-q37/atlas-perl>
- *Ruby*: <http://github.com/epeios-q37/atlas-ruby>



**If you are looking for the *WebGPIO* application, an application with which you can control the Raspberry Pi (or other similar devices) GPIO with your smartphone, you will find it at the bottom of this page, in the *Raspberry Pi*/*ODROID-C2* section.**

---

With the [*Atlas* toolkit](http://atlastk.org/), it has never been easier to create your own modern web application ([*SPA*](https://q37.info/s/7sbmxd3j)):
- no *Javascript* to write; only *HTML* and *Python*,
- no [front and back end architecture](https://q37.info/s/px7hhztd) to bother with,
- no [web server](https://q37.info/s/n3hpwsht) (*Apache*, *Nginx*…) to install,

and all this only with the help of a library of about 20 KB.

With the *Atlas* toolkit, your applications will be accessible from the entire internet on laptops, smartphones, tablets…, and this without having to deploy them on a remote server or to open an incoming port on your internet box. All you need is a local computer with a simple internet connection. 

The *Atlas* toolkit is also the fastest and easiest way to add a [graphical user interface](https://q37.info/s/hw9n3pjs) to all your programs.

If you want to use the *Atlas* toolkit without installing the examples, simply install the [*atlastk* package from *PyPI*](http://q37.info/s/9srmskcm) (`pip install atlastk`). This package has no dependencies.

The *Atlas* toolkit can also be used for educational purposes, to write modern programming exercises, i.e. with a true graphical interface instead of the usual outdated textual one. More about this can be found [here](https://q37.info/s/cbms43s9).

There is also a stub to for this library at address <https://q37.info/s/zzcn3wnx>.

## Live demonstrations

Before diving into source code, you can take a look on some live demonstrations to see how applications based on the *Atlas* toolkit look like. You will find some games, like the [*15-puzzle* game](http://q37.info/s/jn9zg3bn) and the [*Reversi* (aka *Othello*) game](http://q37.info/s/zz3dzmf7). And you will also find the *Atlas* toolkit version of the [*TodoMVC*](http://todomvc.com/) application, which looks like:

![TodoMVC](https://q37.info/download/TodoMVC.gif "The TodoMVC application made with the Atlas toolkit")

To see all this live demonstrations, simply go [here](https://q37.info/s/vwpsw73v), click on the green `run` button, select the demonstration you want to see, and then click (or scan with your smartphone) the then displayed [QR code](https://q37.info/s/3pktvrj7).

## *Hello, World!*

Here's how the [*Hello, World!*](https://en.wikipedia.org/wiki/%22Hello,_World!%22_program) program made with the *Atlas* toolkit looks like:

![Little demonstration](https://q37.info/download/assets/Hello.gif "A basic example")

This example is part of the live demonstrations above, but you can launch it on your computer:

- `git clone http://github.com/epeios-q37/atlas-python`
- `cd atlas-python`
- `python Hello/Hello.py`

You can also put below source code in a file and launch it after having installed the [*atlastk* package](http://q37.info/s/9srmskcm) (`pip install atlastk`), or, with absolutely nothing to install, by pasting and launch the below code [here](http://q37.info/s/srnnb7hj), and then open the displayed *URL* in a web browser.

Source code:

```python
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

def acConnect(dom):
  dom.setLayout("", body)
  dom.focus("input")

def acSubmit(dom):
  dom.alert("Hello, " + dom.getContent("input") + "!")
  dom.focus("input")

def acClear(dom):
  if ( dom.confirm("Are you sure?") ):
    dom.setContent("input", "")
  dom.focus("input")

callbacks = {
  "": acConnect,  # The action label for a new connection is an empty string.
  "Submit": acSubmit,
  "Clear": acClear,
}

Atlas.launch(callbacks)
```

## Content of the repository

The `atlastk` directory contains the *Python* source code of the *Atlas* toolkit, which is the directory you have to reference in `PYTHONPATH` in order to use the *Atlas* toolkit in your own program, unless you have installed the [*atlastk* package](http://q37.info/s/9srmskcm) with `pip install atlastk`.

All other directories are examples:

- *Blank*: very basic example,
- *Hello*: ["*Hello, World!*"](https://en.wikipedia.org/wiki/%22Hello,_World!%22_program),
- *Chatroom*: multi-user chatroom,
- *ReversiTXT*: [*Reversi game*](http://q37.info/s/zz3dzmf7) with `X` and `O` for token,
- *Notes*: note taking program,
- *TodoMVC*: [*TodoMVC*](http://todomvc.com/),
- *Hangman*: [Hangman game](http://q37.info/s/gtdtk4hp),
- *15-puzzle*: [*15-puzzle* game](https://q37.info/s/jn9zg3bn),
- *ReversiIMG*: [*Reversi game*](http://q37.info/s/zz3dzmf7) with more evolved graphics,
- *ReversiXSL*: [*Reversi game*](http://q37.info/s/zz3dzmf7) using *XSL*.

Other exemples are detailed in the next section.

Except for the *ErgoJr*, *GPIO* and *RGB* applications, which are detailed in the next section, to run an example, launch `python main.py`, and select the example you want to run. You can also  launch `python <Name>/` (don't forget the final `/`), where `<Name>` is the name of the example (`Blank`, `Chatroom`…).

The *Stars* application is an example where the *Atlas* *toolkit* is used to control a [*Pygame*](https://en.wikipedia.org/wiki/Pygame) based application. Of course, *Pygame* needs to be installed.

## *Raspberry Pi*/*ODROID-C2*

**If the applications does not work on your *Raspberry Pi*, please see this issue: <https://github.com/epeios-q37/atlas-python/issues/1>**

The *GPIO* and *RGB* applications are designed to be used on a *Raspberry Pi* or a *ODROID-C2*.

For the *Raspberry Pi*, the `RPi.GPIO` *Python* module have to be installed (this is probably already the case).

For the *ODROID-C2*, The *Python* version of *WiringPi* must be installed, and the application has to be launched with `sudo` (`sudo python GPIO/` or `sudo python RGB/`).

The *ErgoJr* application is experimental and to control a *Poppy* *Ergo Jr* robot.

The *RGB* application is dedicated to the control of a RGB led, and the *GPIO* (aka *WebGPIO*) application allows to control the basic pins. Here is a video to see how they works:

[![RGB video](https://img.youtube.com/vi/C4p2iX6gc-Q/0.jpg)](https://www.youtube.com/watch?v=C4p2iX6gc-Q)

Same video on [*PeerTube*](https://en.wikipedia.org/wiki/PeerTube) : <https://peertube.video/videos/watch/e7e02356-c9c3-4590-8ec0-8f8da06ff312>



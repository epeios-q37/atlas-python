# *Python* version of the *Atlas* toolkit

![For Python](https://q37.info/download/assets/Python.png "Python logo")

[![Run on Repl.it](https://repl.it/badge/github/epeios-q37/atlas-python)](https://q37.info/s/vwpsw73v)
[![Version 0.11](https://img.shields.io/static/v1.svg?&color=90b4ed&label=Version&message=0.11)](http://github.com/epeios-q37/atlas-python/)
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

## *Hello, World!*

### Source code

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

### Result

[![Little demonstration](https://q37.info/download/assets/Hello.gif "A basic example")](https://q37.info/s/vwpsw73v)

### Try it yourself now

See the below online demonstrations section, or launch:

- `git clone http://github.com/epeios-q37/atlas-python`
- `python atlas-python/examples/Hello/`

## Online demonstrations

Thanks to [Replit](https://q37.info/s/mxmgq3qm), an [online IDE](https://q37.info/s/zzkzbdw7), you can write and run programs using the *Atlas* toolkit directly in your web browser, without having to install *Python* on your computer.

To see some examples, like the following [*TodoMVC*](http://todomvc.com/) application or the above [*Hello, World!*](https://en.wikipedia.org/wiki/%22Hello,_World!%22_program) program, simply go [here](https://q37.info/s/vwpsw73v), click on the green `run` button, select the demonstration you want to see, and then click (or scan with your smartphone) the then displayed [QR code](https://q37.info/s/3pktvrj7).

[![TodoMVC](https://q37.info/download/TodoMVC.gif "The TodoMVC application made with the Atlas toolkit")](https://q37.info/s/vwpsw73v)

## What do you want to do today?

If you want to:

- take your code to the next level, from [CLI](https://q37.info/s/cnh9nrw9) to [GUI](https://q37.info/s/hw9n3pjs),
- teach your students to program a GUI, 
- impress your teacher with a blowing GUI,
- easily share your programs with all you family and friends,

then you found the right toolkit.

With the [*Atlas* toolkit](http://atlastk.org/), writing modern web applications ([*SPA*](https://q37.info/s/7sbmxd3j)) has never been this easy:
- no *Javascript* to write; only *HTML* and *Python*,
- no [front and back end architecture](https://q37.info/s/px7hhztd) to bother with,
- no [web server](https://q37.info/s/n3hpwsht) (*Apache*, *Nginx*…) to install,
- no need to deploy your application on a remote server,
- no incoming port to open on your internet box.

The *Atlas* toolkit is written in pure *Python* (compatible with version 2 and 3), with no native code and no dependencies, allowing the *Atlas* toolkit to be used on all environments where *Python* is available. 

Simply by running them on a local computer with a simple internet connexion, applications using the *Atlas* toolkit will be accessible from the entire internet on laptops, smartphones, tablets…

The *Atlas* toolkit is particularly well suited for educational purposes, to write modern programming exercises, i.e. with a true graphical interface instead of the usual outdated textual one. More about this can be found [here](https://q37.info/s/cbms43s9).

There is also a stub to for this library at address <https://q37.info/s/zzcn3wnx>.

## Content of the repository

The `atlastk` directory contains the *Python* source code of the *Atlas* toolkit, which is the directory you have to reference in `PYTHONPATH` in order to use the *Atlas* toolkit in your own program, unless you have installed the [*atlastk* package](http://q37.info/s/9srmskcm) with `pip install atlastk`.

In the `examples` directory, you will found following examples:

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

Other examples are detailed in the next section.

Except for the *ErgoJr*, *GPIO* and *RGB* applications, which are detailed in the next section, to run an example, launch, from within the repository, `python main.py`, and select the example you want to run. You can also directly launch `python examples/<Name>/` (don't forget the final `/`), where `<Name>` is the name of the example (`Blank`, `Chatroom`…).

The *Stars* application is an example where the *Atlas* *toolkit* is used to control a [*Pygame*](https://en.wikipedia.org/wiki/Pygame) based application. Of course, *Pygame* needs to be installed.

## *Raspberry Pi*/*ODROID-C2*

**If the applications does not work on your *Raspberry Pi*, please see this issue: <https://github.com/epeios-q37/atlas-python/issues/1>**

The *GPIO* and *RGB* applications are designed to be used on a *Raspberry Pi* or a *ODROID-C2*.

For the *Raspberry Pi*, the `RPi.GPIO` *Python* module have to be installed (this is probably already the case).

For the *ODROID-C2*, The *Python* version of *WiringPi* must be installed, and the application has to be launched, from within the repository, with `sudo` (`sudo python examples/GPIO/` or `sudo python examples/RGB/`).

The *ErgoJr* application is experimental and to control a *Poppy* *Ergo Jr* robot.

The *RGB* application is dedicated to the control of a RGB led, and the *GPIO* (aka *WebGPIO*) application allows to control the basic pins. Here is a video to see how they works:

[![RGB video](https://img.youtube.com/vi/C4p2iX6gc-Q/0.jpg)](https://www.youtube.com/watch?v=C4p2iX6gc-Q)

Same video on [*PeerTube*](https://en.wikipedia.org/wiki/PeerTube) : <https://peertube.video/videos/watch/e7e02356-c9c3-4590-8ec0-8f8da06ff312>



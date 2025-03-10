<div align="center">

The *Atlas* toolkit is available for:

[![Java](https://s.q37.info/jrnv4mj4.svg)](https://github.com/epeios-q37/atlas-java) [![Node.js](https://s.q37.info/fh7v7kn9.svg)](https://github.com/epeios-q37/atlas-node) [![Perl](https://s.q37.info/hgnwnnn3.svg)](https://github.com/epeios-q37/atlas-perl) [![Python](https://s.q37.info/94937nbb.svg)](https://github.com/epeios-q37/atlas-python) [![Ruby](https://s.q37.info/zn4qrx9j.svg)](https://github.com/epeios-q37/atlas-ruby)

To see the *Atlas* toolkit in action:

[![Online demonstrations](https://img.shields.io/static/v1.svg?&color=blue&labelColor=red&label=online&message=demonstrations&style=for-the-badge)](https://s.q37.info/sssznrb4)

</div>

> [*Zelbinium*](http://zelbinium.q37.info): IT for all (especially for teenagers).
>
> Use the *Atlas* toolkit to remotely control microcontrollers like the *ESP32*, *ESP8266*, *Raspberry Pi Pico (2) W*: [*UCUq*](https://s.q37.info/7zrtt9xc).

# *Python* version of the *Atlas* toolkit

<div align="center">

[![Version 0.13](https://img.shields.io/static/v1.svg?&color=90b4ed&label=Version&message=0.13&style=for-the-badge)](http://github.com/epeios-q37/atlas-python/) [![license: MIT](https://img.shields.io/github/license/epeios-q37/atlas-python?color=yellow&style=for-the-badge)](https://github.com/epeios-q37/atlas-python/blob/master/LICENSE) [![Documentation](https://img.shields.io/static/v1?label=documentation&message=atlastk.org&color=ff69b4&style=for-the-badge)](https://atlastk.org) [![Version](https://img.shields.io/pypi/v/atlastk?style=for-the-badge&color=90b4ed&label=PyPi)](http://s.q37.info/9srmskcm)

</div>

## A GUI with *Python* in a couple of minutes

Click the animation to see a screencast of programming this ["Hello, World!" program](https://en.wikipedia.org/wiki/%22Hello,_World!%22_program) with *Python* in a matter of minutes:

<div align="center">

[![Building a GUI in with *Python* in less then 10 minutes](https://s.q37.info/qp4z37pg.gif)](https://s.q37.info/rt9wr4w3)

</div>

Same video on [*Peertube*](https://en.wikipedia.org/wiki/PeerTube): <https://s.q37.info/qfcng9j4>.

<details>
<summary>Click to see the corresponding source code</summary>

```python
import atlastk
 
BODY = """
<fieldset>
 <input id="Input" xdh:onevent="Submit" value="World"/>
 <button xdh:onevent="Submit">Hello</button>
 <hr/>
 <fieldset>
  <output id="Output">Greetings displayed here!</output>
 </fieldset>
</fieldset>
"""
 
def atk(dom): # Callback called on new connections.
  dom.inner("", BODY)
  dom.focus("Input")
 
def atkSubmit(dom): # Callback for the 'Submit' action, hence the name.
  name = dom.getValue("Input")
  dom.begin("Output", f"<div>Hello, {name}!</div>")
  dom.setValue("Input", "")
  dom.focus("Input")
 
atlastk.launch(globals=globals())
```

</details>

### See for yourself right now - it's quick and easy!

```shell
# You can replace 'github.com' with 'framagit.org' or 'gitlab.com'.
# DON'T copy/paste this and above line!
git clone http://github.com/epeios-q37/atlas-python
cd atlas-python/examples
python Hello/
```

## *Android* devices

Applications made with the *Atlas* toolkit work perfectly on your [*Android*](https://en.wikipedia.org/wiki/Android_(operating_system)) devices (smartphone or tablet) using the [*Termux*](https://termux.com/) application. Simply install (``pkg intall …``) the *git* and *python* packages. That's all!

## *Jupyter* notebooks

When using the *Atlas* toolkit in a [*Jupyter* notebook](https://en.wikipedia.org/wiki/Project_Jupyter#Jupyter_Notebook), the GUI is embedded in the notebook, as shown here:

<div align="center">

![](https://s.q37.info/f7qqvhs3.gif)

</div>

*Jupyter* notebook examples can be found in the *tutorials* directory.

## Your turn

If you want to take your code to the next level, from [CLI](https://s.q37.info/cnh9nrw9) to [GUI](https://s.q37.info/hw9n3pjs), then you found the right toolkit.

With the [*Atlas* toolkit](http://atlastk.org/), you transform your programs in modern web applications ([*SPA*](https://s.q37.info/7sbmxd3j)) without the usual hassles:
- no *JavaScript* to write; only *HTML*(/*CSS*) and *Python*,
- no [front and back end architecture](https://s.q37.info/px7hhztd) to bother with,
- no [web server](https://s.q37.info/n3hpwsht) (*Apache*, *Nginx*…) to install,
- no need to deploy your application on a remote server,
- no incoming port to open on your internet box or routeur.

The *Atlas* toolkit is written in pure *Python*, with no native code and no dependencies, allowing the *Atlas* toolkit to be used on all environments where *Python* is available. 

And simply by running them on a local computer connected to internet, applications using the *Atlas* toolkit will be accessible from the entire internet on laptops, smartphones, tablets…

The *Atlas* toolkit is particularly well suited for educational purposes, to write modern programming exercises, i.e. with a true graphical interface instead of the usual old-looking textual one. More about this can be found [here](https://s.q37.info/cbms43s9).

*Python* is much more powerful then *Excel* macros to automate (boring) tasks, and you can also work with *PDF*, *Word*, *Google* files…. And with the *Atlas* toolkit, you have much more possibilities then with *VBA* forms. There are some examples [here](https://s.q37.info/97p44nh4).

> You will also find programs from [*The Big Book of Small Python Projects*](https://inventwithpython.com/bigbookpython/) by [Al Sweigart](http://alsweigart.com) to which a graphical user interface using the *Atlas* toolkit were added in this repository: [epeios-q37/AlSweigartTheBigBookPython](https://s.q37.info/kd3bwchj).

## Content of the repository

The `atlastk` directory contains the *Python* source code of the *Atlas* toolkit, which is the directory you have to reference in `PYTHONPATH` in order to use the *Atlas* toolkit in your own program, unless you have installed the [*atlastk* package](http://s.q37.info/9srmskcm) (`pip install atlastk`…).

You can also retrieve the `atlastk.zip` file, and add to your source code :

```python
__import__("sys").path.append("<path to>/atlastk.zip")

import atlastk
```

If the `atlastk.zip` file is in the current folder, replace `<path-to>/atlastk.zip` with `./atlastk.zip` and not only `atlastk.zip`.

In the `examples` directory, you will found following examples:

- `Blank`: very basic example,
- `Hello`: ["*Hello, World!*"](https://en.wikipedia.org/wiki/%22Hello,_World!%22_program),
- `Chatroom`: multi-user chatroom,
- `Notes`: note taking program,
- `TodoMVC`: [*TodoMVC*](http://todomvc.com/),
- `Hangman`: [Hangman game](http://s.q37.info/gtdtk4hp),
- `15-puzzle`: [15-puzzle game](https://s.q37.info/jn9zg3bn),
- `Contacts`: a basic address book, 
- `Widgets`: some widgets handled with the *Atlas* toolkit,
- `Chatrooms` : same as above `Chatroom`, but with several rooms,
- `PigGame`: [Pig game](https://en.wikipedia.org/wiki/Pig_(dice_game)) for one or two players,
- `Reversi`: [*Reversi* game](http://s.q37.info/zz3dzmf7) for one or two players,
- `MatPlotLib` : the *Atlas* toolkit displaying some graphics made with [*matplotlib*](https://matplotlib.org/); this example needs, of course, the *matplotlib* package to be installed…

Other examples are detailed in the next section.

Except for the *ErgoJr*, *GPIO* and *RGB* applications, which are detailed in the next section, to run an example, launch, from within the `examples` directory, `python <Name>/` (don't forget the final `/`), where `<Name>` is the name of the example (`Blank`, `Chatroom`…).

The *Stars* application is an example where the *Atlas* *toolkit* is used to control a [*Pygame*](https://en.wikipedia.org/wiki/Pygame) based application. Of course, *Pygame* needs to be installed.

The `tutorials` directory contains some [*Jupyter* notebooks](https://en.wikipedia.org/wiki/Project_Jupyter#Jupyter_Notebook) about  the *Atlas* *toolkit*.

## *Raspberry Pi*/*ODROID-C2*

**If the applications does not work on your *Raspberry Pi*, please see this issue: <https://github.com/epeios-q37/atlas-python/issues/1>**

The *GPIO* and *RGB* applications are designed to be used on a *Raspberry Pi* or a *ODROID-C2*.

Here is how the *WebGPIO* application looks like:

<div align="center">

![*WebGPIO* interface](https://s.q37.info/htkhqb9x.png)

</div>

For the *Raspberry Pi*, the `RPi.GPIO` *Python* module have to be installed (this is probably already the case).

For the *ODROID-C2*, The *Python* version of *WiringPi* must be installed, and the application has to be launched, from within the `examples` directory, with `sudo` (`sudo python GPIO/` or `sudo python RGB/`).

The *ErgoJr* application is experimental and to control a *Poppy* *Ergo Jr* robot.

The *RGB* application is dedicated to the control of a RGB led, and the *GPIO* (aka *WebGPIO*) application allows to control the basic pins. Click below picture to see a *YouTube* video on how they work (same video on [*PeerTube*](https://en.wikipedia.org/wiki/PeerTube): <https://s.q37.info/49pbmwv9>):

<div align="center">

[![RGB video](https://img.youtube.com/vi/C4p2iX6gc-Q/0.jpg)](https://www.youtube.com/watch?v=C4p2iX6gc-Q)

</div>



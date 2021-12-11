# *Python* version of the *Atlas* toolkit

[![Run on Repl.it](https://q37.info/s/kpm7xhfm.png)](https://q37.info/s/vwpsw73v)  [![About online demonstrations](https://img.shields.io/badge/about-online%20demonstrations-informational)](https://q37.info/s/sssznrb4)

[![Version 0.13](https://img.shields.io/static/v1.svg?&color=90b4ed&label=Version&message=0.13&style=for-the-badge)](http://github.com/epeios-q37/atlas-python/)
[![license: MIT](https://img.shields.io/github/license/epeios-q37/atlas-python?color=yellow&style=for-the-badge)](https://github.com/epeios-q37/atlas-python/blob/master/LICENSE)
[![Documentation](https://img.shields.io/static/v1?label=documentation&message=atlastk.org&color=ff69b4&style=for-the-badge)](https://atlastk.org)  

[![Version](https://img.shields.io/pypi/v/atlastk?style=for-the-badge&color=90b4ed&label=PyPi)](http://q37.info/s/9srmskcm)

<!--
Si la table ci-dessous est modifiée, alors modifier également (pages du site atlastk.org) :
- la page 'Home' ;
- la page 'Online demonstrations' ;
-->

> The [*Atlas* toolkit](https://atlastk.org) is available for:
> | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Language | Online demonstrations | Repo. #1 | #2 | #3 |Stars
> |-|-|:-:|:-:|:-:|:-:|:-:|
> | ![Java](https://q37.info/s/sgb9nq7x.svg) | [*Java*](https://q37.info/s/qtnkp9w4)  | [![Run on Replit](https://q37.info/s/kpm7xhfm.png)](https://q37.info/s/3vwk3h3n) | [*Framagit*](https://framagit.org/epeios-q37/atlas-java) | [*GitHub*](https://github.com/epeios-q37/atlas-java) | [*GitLab*](https://gitlab.com/epeios-q37/atlas-java) | [![Stars for atlas-java](https://img.shields.io/github/stars/epeios-q37/atlas-java.svg?label=)](https://github.com/epeios-q37/atlas-java/stargazers)
> | ![Node.js](https://q37.info/s/b9ctj4bb.svg) | [*Node.js*](https://q37.info/s/3d7hr733) | [![Run on Replit](https://q37.info/s/kpm7xhfm.png)](https://q37.info/s/st7gccd4) | [*Framagit*](https://framagit.org/epeios-q37/atlas-node) | [*GitHub*](https://github.com/epeios-q37/atlas-node) | [*GitLab*](https://gitlab.com/epeios-q37/atlas-node) | [![Stars for atlas-node](https://img.shields.io/github/stars/epeios-q37/atlas-node.svg?label=)](https://github.com/epeios-q37/atlas-node/stargazers)
> | ![Perl](https://q37.info/s/v9qkzvhk.svg) | [*Perl*](https://q37.info/s/4nvmwjgg)  | [![Run on Replit](https://q37.info/s/kpm7xhfm.png)](https://q37.info/s/h3h34zgq) | [*Framagit*](https://framagit.org/epeios-q37/atlas-perl) | [*GitHub*](https://github.com/epeios-q37/atlas-perl) | [*GitLab*](https://gitlab.com/epeios-q37/atlas-perl) | [![Stars for atlas-perl](https://img.shields.io/github/stars/epeios-q37/atlas-perl.svg?label=)](https://github.com/epeios-q37/atlas-perl/stargazers)
> | ![Python](https://q37.info/s/t4s3p4rk.svg) | [*Python*](https://q37.info/s/pd7j9k4r)  | [![Run on Replit](https://q37.info/s/kpm7xhfm.png)](https://q37.info/s/vwpsw73v) | [*Framagit*](https://framagit.org/epeios-q37/atlas-python) | [*GitHub*](https://github.com/epeios-q37/atlas-python)  | [*GitLab*](https://gitlab.com/epeios-q37/atlas-python) | [![Stars](https://img.shields.io/github/stars/epeios-q37/atlas-python.svg?label=)](https://github.com/epeios-q37/atlas-python/stargazers)
> | ![Ruby](https://q37.info/s/ngxztq4t.svg) | [*Ruby*](https://q37.info/s/gkfj3zpz)  | [![Run on Replit](https://q37.info/s/kpm7xhfm.png)](https://q37.info/s/9thdtmjg) | [*Framagit*](https://framagit.org/epeios-q37/atlas-ruby) | [*GitHub*](https://github.com/epeios-q37/atlas-ruby) | [*GitLab*](https://gitlab.com/epeios-q37/atlas-ruby) | [![Stars for atlas-ruby](https://img.shields.io/github/stars/epeios-q37/atlas-ruby.svg?label=)](https://github.com/epeios-q37/atlas-ruby/stargazers)

<ins>***WebGPIO* (*Raspberry Pi*/*ODROID-C2*)**</ins>: the *WebGPIO* application, with which you can control the *Raspberry Pi*/*ODROID-C2* (and probably other similar devices) GPIOs with your smartphone, is described in the *Raspberry Pi*/*ODROID-C2* below section.



---

## A GUI with *Python* in a couple of minutes

Click the animation to see a screencast of programming this ["Hello, World!" program](https://en.wikipedia.org/wiki/%22Hello,_World!%22_program) with *Python* in a matter of minutes:

[![Building a GUI in with *Python* in less then 10 minutes](https://q37.info/s/qp4z37pg.gif)](https://q37.info/s/rt9wr4w3)

Same video on [*Peertube*](https://en.wikipedia.org/wiki/PeerTube): <https://q37.info/s/qfcng9j4>.

Source code:

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
 
def ac_connect(dom):
  dom.inner("", BODY)
  dom.focus("Input")
 
def ac_submit(dom):
  name = dom.get_value("Input")
  dom.begin("Output", f"<div>Hello, {name}!</div>")
  dom.set_value("Input", "")
  dom.focus("Input")
 
CALLBACKS = {
  "": ac_connect,
  "Submit": ac_submit
}
 
atlastk.launch(CALLBACKS)
```

### See for yourself right now - it's quick and easy!

#### Online, with nothing to install

To run above "Hello, World!" program directly in your browser, as seen in corresponding video, follow this link: <https://replit.com/@AtlasTK/hello-python>.

Thanks to [*Replit*](https://q37.info/s/mxmgq3qm), an [online IDE](https://q37.info/s/zzkzbdw7), you can write and run programs using the *Atlas* toolkit directly in your web browser, without having to install *Python* on your computer [![About online demonstrations](https://img.shields.io/badge/about-online%20demonstrations-informational)](https://q37.info/s/sssznrb4).

To see more examples, like the following [*TodoMVC*](http://todomvc.com/), simply:
- go [here](https://q37.info/s/vwpsw73v) (also accessible with the [![Run on Repl.it](https://q37.info/s/kpm7xhfm.png)](https://q37.info/s/vwpsw73v) button at the top of this page),
- click on the green `run` button,
- choose the demonstration to launch,
- open the then displayed URL in a browser (should be clickable), 
- … and, as you wish, run your own tests directly in your browser, by modifying the code of the examples or by writing your own code.

[![TodoMVC](https://q37.info/download/TodoMVC.gif "The TodoMVC application made with the Atlas toolkit")](https://q37.info/s/vwpsw73v)

#### With *Python* on your computer

```shell
# You can replace 'github.com' with 'framagit.org' or 'gitlab.com'.
# DON'T copy/paste this and above line!
git clone http://github.com/epeios-q37/atlas-python
cd atlas-python/examples
python Hello/
```

## *Android* devices

Programs made with the *Atlas* toolkit work perfectly on your [*Android*](https://en.wikipedia.org/wiki/Android_(operating_system)) devices (smartphone or tablet) using the [*Termux*](https://termux.com/) application. Simply install (``pkg intall …``) the *git* and *python* packages. That's all!

## *Jupyter* notebooks

When using the *Atlas* toolkit in a [*Jupyter* notebook](https://en.wikipedia.org/wiki/Project_Jupyter#Jupyter_Notebook), the GUI is embedded in the notebook, as shown here:

![](https://q37.info/s/f7qqvhs3.gif)

*Jupyter* notebook examples can be found in the *tutorials* directory.

## Your turn

If you want to take your code to the next level, from [CLI](https://q37.info/s/cnh9nrw9) to [GUI](https://q37.info/s/hw9n3pjs), then you found the right toolkit.

With the [*Atlas* toolkit](http://atlastk.org/), you transform your programs in modern web applications ([*SPA*](https://q37.info/s/7sbmxd3j)) without the usual hassles:
- no *JavaScript* to write; only *HTML*(/*CSS*) and *Python*,
- no [front and back end architecture](https://q37.info/s/px7hhztd) to bother with,
- no [web server](https://q37.info/s/n3hpwsht) (*Apache*, *Nginx*…) to install,
- no need to deploy your application on a remote server,
- no incoming port to open on your internet box or routeur.

The *Atlas* toolkit is written in pure *Python*, with no native code and no dependencies, allowing the *Atlas* toolkit to be used on all environments where *Python* is available. 

And simply by running them on a local computer connected to internet, applications using the *Atlas* toolkit will be accessible from the entire internet on laptops, smartphones, tablets…

The *Atlas* toolkit is particularly well suited for educational purposes, to write modern programming exercises, i.e. with a true graphical interface instead of the usual outdated textual one. More about this can be found [here](https://q37.info/s/cbms43s9).

*Python* is much more powerful then *Excel* macros to automate (boring) tasks, and you can also work with *PDF*, *Word*, *Google* files…. And with the *Atlas* toolkit, you have much more possibilities then with *VBA* forms. There are some examples [here](https://q37.info/s/97p44nh4).  

There is also a stub to for this library at address <https://q37.info/s/zzcn3wnx>.

## Content of the repository

The `atlastk` directory contains the *Python* source code of the *Atlas* toolkit, which is the directory you have to reference in `PYTHONPATH` in order to use the *Atlas* toolkit in your own program, unless you have installed the [*atlastk* package](http://q37.info/s/9srmskcm) with `pip install atlastk`.

In the `examples` directory, you will found following examples:

- `Blank`: very basic example,
- `Hello`: ["*Hello, World!*"](https://en.wikipedia.org/wiki/%22Hello,_World!%22_program),
- `Chatroom`: multi-user chatroom,
- `Notes`: note taking program,
- `TodoMVC`: [*TodoMVC*](http://todomvc.com/),
- `Hangman`: [Hangman game](http://q37.info/s/gtdtk4hp),
- `15-puzzle`: [15-puzzle game](https://q37.info/s/jn9zg3bn),
- `Contacts`: a basic address book, 
- `Widgets`: some widgets handled with the *Atlas* toolkit,
- `Chatrooms` : same as above `Chatroom`, but with several rooms,
- `PigGame`: [Pig game](https://en.wikipedia.org/wiki/Pig_(dice_game)) for one or two players,
- `Reversi`: [*Reversi* game](http://q37.info/s/zz3dzmf7) for one or two players,
- `MatPlotLib` : the *Atlas* toolkit displaying some graphics made with [*matplotlib*](https://matplotlib.org/); this example needs, of course, the *matplotlib* package to be installed…

Other examples are detailed in the next section.

Except for the *ErgoJr*, *GPIO* and *RGB* applications, which are detailed in the next section, to run an example, launch, from within the repository, `python main.py`, and select the example you want to run.  
You can also directly launch, from within the `examples` directory, `python <Name>/` (don't forget the final `/`), where `<Name>` is the name of the example (`Blank`, `Chatroom`…).

The *Stars* application is an example where the *Atlas* *toolkit* is used to control a [*Pygame*](https://en.wikipedia.org/wiki/Pygame) based application. Of course, *Pygame* needs to be installed.

The `tutorials` directory contains some [*Jupyter* notebooks](https://en.wikipedia.org/wiki/Project_Jupyter#Jupyter_Notebook) about  the *Atlas* *toolkit*. 

## *Raspberry Pi*/*ODROID-C2*

**If the applications does not work on your *Raspberry Pi*, please see this issue: <https://github.com/epeios-q37/atlas-python/issues/1>**

The *GPIO* and *RGB* applications are designed to be used on a *Raspberry Pi* or a *ODROID-C2*.

Here is how the *WebGPIO* application looks like:

![*WebGPIO* interface](https://q37.info/s/htkhqb9x.png)

For the *Raspberry Pi*, the `RPi.GPIO` *Python* module have to be installed (this is probably already the case).

For the *ODROID-C2*, The *Python* version of *WiringPi* must be installed, and the application has to be launched, from within the `examples` directory, with `sudo` (`sudo python GPIO/` or `sudo python RGB/`).

The *ErgoJr* application is experimental and to control a *Poppy* *Ergo Jr* robot.

The *RGB* application is dedicated to the control of a RGB led, and the *GPIO* (aka *WebGPIO*) application allows to control the basic pins. Click below picture to see a *YouTube* video on how they work (same video on [*PeerTube*](https://en.wikipedia.org/wiki/PeerTube): <https://q37.info/s/49pbmwv9>):

[![RGB video](https://img.youtube.com/vi/C4p2iX6gc-Q/0.jpg)](https://www.youtube.com/watch?v=C4p2iX6gc-Q)



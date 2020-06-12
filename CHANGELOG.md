# *CHANGELOG* for the *Atlas* toolkit

- Common to **all** bindings,
- does **not** concern the native code,

## 2020-06-12

- *ALL*:
    - switching to 0.11,

## 2019-08-01

- *Python*
  - switching to 0.10.7,

## 2019-07-31

- *Python*:
  - if the `userCallback` parameter of the `Launch(…)` function is or returns `None`, the (optional) first parameter passed to the callbacks will be the *DOM* object (which is otherwise passed as second parameter, the user object returned by the user callback being the first),

## 2019-07-28

- *Python*:
  - the user callback can now be `None`,

## 2019-07-26

- *Python*:
  - switching to 0.10.4,

## 2019-07-17

- *Python*:
  - *CTRL-C* does no more display messages,

## 2019-07-09

- *Python*:
  - fixing encoding issue under *Python* 2,
  - using ordered dictionaries under *Python* 2, to facilitate the retrieving of values, by using `values()` method, with methods returning dictionaries (dictionaries are ordered by default under *Python* 3),

## 2019-07-08

- *ALL*:
    - switching to 0.10.0,

## 2019-07-03

- *Perl*
  - updating the *API* to fit with the version 0.9 (not documented yet),
  - switching to 0.9.0,
  - (adding the *Notes* application),
- *Python*:
  - fixing issue that prevented the toolkit from working with *Python* 2,
  - switching to 0.9.9

## 2019-07-01

- *Python*:
  - the callbacks can now have none to four (user object, *DOM* object, id, action) parameters,
  - switching to 0.9.8

## 2019-06-01

- *Python*:
  - adding CSS rules related functions,
  - user callback to create new user object is now called from same thread as the action callbacks (fixes issue with *sqlite3*, which prevents the use of the constructor to initialize a db),
  - HTML data sent to `setLayout(…)` function does no more require a unique root tag,
  - switching to 0.9.7,

## 2019-05-22

- *Python*:
  - `createHTML(…)` can now be used with no parameters, in which case only the children are used,
  - new `setTag(…)` function for the XML/HTML tree,

## 2019-05-09

- *Node.js*:
  - changing some stuff related to *Repl.it*,
  - switching to 0.9.2,

## 2019-05-07

- *Python*:
  - `setLayoutXSL(…)` can now take a string containing the XSL data,
  - switching to 0.9.6,

## 2019-05-02

- *Python*:
  - modification of the *Repl.it* related stuff,
  - `CreateHTML(…)` becomes an alias of `CreateXML(…)`,
  - switching to 0.9.5

## 2019-04-30

- *Node.js*:
  - adding some features related to *Repl.it*,
  - switching to 0.9.1
- *Python*:
  - adding some features related to *Repl.it*,
  - switching to 0.9.4

## 2019-04-24

- *Python*:
  - modifications to fit with *Pypi*,
  - switching to 0.9.1,

## 2019-04-18

- switching to 0.9.0 due to a *RunKit* issue,

## 2019-04-17

- *Node.js*, *Python*:
  - switching to 0.8.0

## 2019-04-16

- *Node.js*, *Python*:
  - `setLayout(...)` accepts now an *XML* (from the *Atlas* toolkit) object in addition to *HTML* string.

## 2019-04-03

- *Ruby*:
  - fixing issues occurring under *POSIX*,
  - switching to version 0.7.1,

## 2019-03-04

- one back-end now only opens one (multiplexed) connection to the proxy, instead of one per session,
- switching to version 0.7,

## 2018-12-22

- the opening of the web browser does no more block the entire app under some *Linux* distribution,

## 2018-12-18

- handling error on token,

## 2018-12-14

- switching to version 0.6,

## 2018-12-11

- removing the new session related stuff,

## 2018-12-07

- *Python*
  - fixing `(set|remove)Attribute(…)` bug,
- **ALL**:
  - switching to new protocol and resetting version,
  - switching to version 5.2,

## 2018-11-24

- *Node.js*:
  - fixing error message displayed when not able to connect,

## 2018-11-23

- *Node.js* and *Python* bindings:
  - fixing error in handling environment variables for proxy/web address/port,
  - switching to version 0.5.1a,

## 2018-11-22

- both application (web) address/port and proxy address/port can now be set with environment variables,
- switching to version 0.5.1,

## 2018-11-20

- switching to protocol version 1,

## 2018-11-18
- *Node.js* binding
  - version 0.5.0b; only to fix a *NPM*/*Github* issue,

## 2018-11-17

- *Node.js* binding:
  - the *URL* is now also automatically opened in a web browser with *Termux* (*Android*),
  - version 0.5.0a

## 2018-11-15

- introducing the *Python* binding,

## 2018-11-09

- version 0.5.0,

## …

## 2018-09-03

- version 0.2.0,

## 2018-08-19

- version  0.1.9,

## 2018-04-20

- *atlas-java*
  - simplification,
- all bindings:
  - version  0.1.0,

## 2018-03-07

- _UnJSq_ becomes _Atlas_ (toolkit),

## 2018-02-03

- adding `execute`, `focus`, `removeAttribute`,

## 2018-01-10

- *unjsq-node*:
    - fixing compilation issues under *macOS*.

---
title: 'Atlas toolkit for Python: adding graphical user interfaces to Python programs'
tags:
  - Python
  - web
  - interface
authors:
  - name: Claude Simon
    orcid: 0000-0002-5928-236X
affiliations:
date: 5 April 2019
---

# Background

The *Atlas* toolkit for *Python* provides a quick and easy way to add a graphical user interface to *Python* programs. The goal is not to compete with all the already existing *GUI* frameworks or toolkits. The *Atlas* toolkit is for those who want their programs to have a *GUI* without spending too much time on it.

# Summary

To use the *Atlas* toolkit, only basic knowledge of *HTML*(/*CSS*) and the [*DOM*](https://en.wikipedia.org/wiki/Document_Object_Model) is required. You don't have to bother with *JavaScript*, as you will program the interface entirely in *Python*. The toolkit is very lightweight (less then 10 KB), and runs flawlessly on low-performance such as the [*Raspberry Pi Zero W*](https://q37.info/s/uthai3us). Even programs which weren't initially designed to have a GUI can easily take advantage of the *Atlas* toolkit (no [*MVC*](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller) architectural pattern to follow).

When a program using the *Atlas* toolkit is launched, its interface will be automatically opened in a web browser. And the program will automagically be accessible from all over internet through its *URL* (also available as [*QR code*](https://en.wikipedia.org/wiki/QR_code)). No need to configure the router on which the computer running the program is connected, and also no need to deploy the program on a remote server.

# Availability

The *Atlas* toolkit for *Python* is available under the *GNU* *AGPL* on <https://github.com/epeios-q37/atlas-python>.

To learn more about the *Atlas* toolkit, see <https://atlastk.org>.

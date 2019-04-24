""" 
MIT License

Copyright (c) 2018 Claude SIMON (https://q37.info/s/rmnmqd49)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import setuptools

version = "0.9.1"

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="atlastk",
    version=version,
    author="Claude SIMON",
#    author_email="author@example.com",
    description="A fast and easy way to add sharable web interfaces to Python programs.",
    keywords="GUI graphical user interface web",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://q37.info/s/c7hfkzvs",
    packages=setuptools.find_packages(),
    project_urls= {
    'Contact': 'http://q37.info/s/ggq7x4w7',
    'Homepage': 'http://atlastk.org',
    'Source': 'http://q37.info/s/c7hfkzvs',
    'API': 'http://q37.info/s/gei0veus',
    },
    classifiers=[
      "Environment :: Web Environment",
      "Development Status :: 5 - Production/Stable",
      "Intended Audience :: Developers",
      "Intended Audience :: Education",
      "Intended Audience :: Other Audience",
      "License :: OSI Approved :: MIT License ",
      "Operating System :: OS Independent",
      "Programming Language :: Python :: 2",
      "Programming Language :: Python :: 3",
      "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
      "Topic :: Software Development :: User Interfaces"
    ]
)
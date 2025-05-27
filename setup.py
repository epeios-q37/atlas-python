import setuptools

version = "0.13.5"

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="atlastk",
    version=version,
    author="Claude SIMON",
#    author_email="author@example.com",
    description="Easily bring your Python applications online with the world's lightest GUI toolkit.",
    keywords="GUI, web, Atlas toolkit, DOM, HTML, browser, multi-user, online, networking, user-interaction, remote-access, instant-access, easy-deploy, Android, Termux, Jupyter, Notebook",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://atlastk.org",
    packages=setuptools.find_packages(),
    classifiers=[
      "Environment :: Web Environment",
      "Development Status :: 5 - Production/Stable",
      "Intended Audience :: Developers",
      "Intended Audience :: Education",
      "Intended Audience :: Other Audience",
      "License :: OSI Approved :: MIT License ",
      "Operating System :: OS Independent",
      "Programming Language :: Python :: 3",
      "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
      "Topic :: Software Development :: User Interfaces"
    ]
)

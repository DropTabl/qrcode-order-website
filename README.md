# QRCode Base Order Website

![Example Image](docs/images/logo.webp)

This project servers the architecture and a website that uses QR codes to place cocktail orders.


Documentation
-------------

The complete documentation can be found on my directory at the [Lehre Server](https://lehre.bpm.in.tum.de/~ge56qon/docs/index.html) or at this
[GitHub Page](https://lehre.bpm.in.tum.de/~ge56qon/docs/index.html)


There are all necessary information to install, configure and use the website. 
Also, the documentation contains information about the used technologies and the architecture of the website as well a
all API endpoints.
There is also a demo section that shows how to use the website and the CPEE.

Structure
---------
All code can be found in the `src` directory.
The `src` directory contains all necessary python files for the different processes.
The `src/PHP` directory that contains PHP code that is needed for some sub 
processes.
The `src/HTML` directory contains the HTML code for the website.

All necessary CPEE models can be found in the `CPEE` directory.

The `docs` directory contains the documentation, which is a sphinx documentation.


Building the documentation locally
----------------------------------

This documentation is built using [Sphinx](http://www.sphinx-doc.org/en/master/).

To build this documentation locally, clone this repo, cd into the docs folder and use the following command:

```bash
pip install -r requirements.txt
cd docs
make html
```

The index page is located at `index.html` in the `_build/html` directory.
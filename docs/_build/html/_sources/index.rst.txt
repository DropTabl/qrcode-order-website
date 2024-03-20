.. QRCodeBaseOrderWebsite documentation master file, created by
   sphinx-quickstart on Mon Mar 18 19:49:34 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

QR-Code Base Order Website Documentation
========================================

.. image:: images/logo.webp
  :alt: alternative text
  :align: center
  :width: 1200



This is the documentation for the QR-Code Base Order Website.
This website is a order website that uses QR codes to place cocktail orders.

The complete documentation can be found on my directory at the `Lehre Server <https://lehre.bpm.in.tum.de/~ge56qon/docs/index.html>`_ or at this `GitHub Page <https://droptabl.github.io/qrcode-order-website/>`_.


Building the documentation locally
----------------------------------

This documentation is built using `Sphinx <http://www.sphinx-doc.org/en/master/>`_.

To build this documentation locally, you can use the following command:

   .. code-block:: bash

      make html

The index page is located at `index.html` in the `_build/html` directory.




Contents
--------
.. toctree::
   :maxdepth: 2
   :caption: General:

   arch
   how_to
   demo

.. toctree::
   :maxdepth: 2
   :caption: API Documentation:

   scheduler
   OMS
   QR_WEB
   Recipe
   Simulator
   Order_Store







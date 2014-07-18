.. _getting_started:


***************
About Tortazo - Gentle Introduction.
***************

.. _installing-docdir:


What?
=============================

Tortazo is a python tool to perform pentesting activities throught the TOR's deep web. Allows the integration with other well known frameworks available in the market and any python developer could write plugins to execute attacks against hidden services.


How?
=============================
Tortazo is written in Python language using a lot of libraries written in Python to perform pentesting activities. This project is almost entirely "I+D" because there's so few tools publicly available in the market focused to pentesting TOR hidden services or even TOR relays. The researching and innovative ideas are much appreciated because, there's a lot of work and thing to implement in Tortazo.


Why?
=============================
Anonymous networks are the favorite "tool" of criminals and this is a shame because networks like TOR, I2P or Freenet weren't designed to protect assessins, pedofiles, narcotraficants and that kind of people. The initial idea of this project, was develop a tool to compromise the identity of that people. ¿How? A lot of them, usually are not aware of the vulnerabilities included in their boxes. A lot of them, just uses tools and publish hidden services with the "defaults" because they're not security profesionals and usually are just end-users with basic knowledge about computing. A lot of them just start TOR and expose their machines as relays in the TOR network or setup websites as TOR hidden services without any security consideration. This is a good "starting point" to try to expose them and the pourpose of Tortazo is to include a lot of features to find that kind of flaws. 


When?
=============================
This project was initiated in early 2014 and actually is being developed just by me (@jdaanial aka. Adastra). Initially was a simple prototipe to test the features included in Stem library for TOR. (https://stem.torproject.org/) 
Stem is a impresive python library which uses the TOR controller protocol to manage a TOR instance. However, also includes utilities to querying the TOR authoritative directories and download the descriptors with the information about the relays running in TOR. On other hand, there's a lot of libraries and tools to perform pentesting activities which will be perfect against some vulnerable web applications in the deep web. 
Tortazo allows the integration from some of the most known of this tools and frameworks 


Who?
=============================
I'm a software developer and security enthusiast. Just a guy who spent his time playing with libraries, programming languages, tools, security techniques, network protocols and anything related with computers :-)
What I like:
I like to read almost about everything.
I like the free speech.
I like free software.
I like the hacker philosophy.
I like the hacktivism.
I like to write code.
I like to find and fix bugs in code.
I like to improve code.
I like the reverse engineering.
I like to talk with people about things that matters. (not about football, politics, tv shows and other bullshit).
I like the freedom. Everyone should be free to do anything, but without affecting the freedom of others.

What I dislike:
I dislike the bugs.
I dislike the awful code.
I dislike the people lazy.
I dislike the mediocrity.
I dislike the authoritarianism. 
I dislike some rock stars "selling smoke" in conferences and other events. We need more mentors and less security rock stars. Sadly, this is the worst thing that I've found in the infosec environment.


Contact?
=============================
Sure, just write an email to: debiadastra [at] gmail.com I'll reply as soon as possible.
Also, you can follow me in Twitter. @jdaanial


OK, are you ready? Go and read about Tortazo and star to use it :file:`getting_started.rst`

You may already have sphinx `sphinx <http://sphinx.pocoo.org/>`_
installed -- you can check by doing::

  python -c 'import sphinx'

If that fails grab the latest version of and install it with::

  > sudo easy_install -U Sphinx

Now you are ready to build a template for your docs, using
sphinx-quickstart::

  > sphinx-quickstart

accepting most of the defaults.  I choose "sampledoc" as the name of my
project.  cd into your new directory and check the contents::

  home:~/tmp/sampledoc> ls
  Makefile	_static		conf.py
  _build		_templates	index.rst

The index.rst is the master ReST for your project, but before adding
anything, let's see if we can build some html::

  make html

If you now point your browser to :file:`_build/html/index.html`, you
should see a basic sphinx site.

.. image:: _static/basic_screenshot.png

.. _fetching-the-data:

Fetching the data
-----------------

Now we will start to customize out docs.  Grab a couple of files from
the `web site <https://github.com/matplotlib/sampledoc>`_
or git.  You will need :file:`getting_started.rst` and
:file:`_static/basic_screenshot.png`.  All of the files live in the
"completed" version of this tutorial, but since this is a tutorial,
we'll just grab them one at a time, so you can learn what needs to be
changed where.  Since we have more files to come, I'm going to grab
the whole git directory and just copy the files I need over for now.
First, I'll cd up back into the directory containing my project, check
out the "finished" product from git, and then copy in just the files I
need into my :file:`sampledoc` directory::

  home:~/tmp/sampledoc> pwd
  /Users/jdhunter/tmp/sampledoc
  home:~/tmp/sampledoc> cd ..
  home:~/tmp> git clone https://github.com/matplotlib/sampledoc.git tutorial
  Cloning into 'tutorial'...
  remote: Counting objects: 87, done.
  remote: Compressing objects: 100% (43/43), done.
  remote: Total 87 (delta 45), reused 83 (delta 41)
  Unpacking objects: 100% (87/87), done.
  Checking connectivity... done
  home:~/tmp> cp tutorial/getting_started.rst sampledoc/
  home:~/tmp> cp tutorial/_static/basic_screenshot.png sampledoc/_static/

The last step is to modify :file:`index.rst` to include the
:file:`getting_started.rst` file (be careful with the indentation, the
"g" in "getting_started" should line up with the ':' in ``:maxdepth``::

  Contents:

  .. toctree::
     :maxdepth: 2

     getting_started.rst

and then rebuild the docs::

  cd sampledoc
  make html


When you reload the page by refreshing your browser pointing to
:file:`_build/html/index.html`, you should see a link to the
"Getting Started" docs, and in there this page with the screenshot.
`Voila!`

Note we used the image directive to include to the screenshot above
with::

  .. image:: _static/basic_screenshot.png


Next we'll customize the look and feel of our site to give it a logo,
some custom css, and update the navigation panels to look more like
the `sphinx <http://sphinx.pocoo.org/>`_ site itself -- see
:ref:`custom_look`.


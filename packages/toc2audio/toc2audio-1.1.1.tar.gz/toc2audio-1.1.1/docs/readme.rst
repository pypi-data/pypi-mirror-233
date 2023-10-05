toc2audio
=========

.. WE CAN NOT DO ".. include::" because it would be not valid for PYPI

.. _HTML: https://en.wikipedia.org/wiki/HTML
.. _markdown: https://en.wikipedia.org/wiki/Markdown

.. _MP3: https://en.wikipedia.org/wiki/MP3
.. _M4A: https://en.wikipedia.org/wiki/MPEG-4_Part_14
.. _MP4: https://en.wikipedia.org/wiki/Mp4
.. _Opus: https://en.wikipedia.org/wiki/Opus_(audio_format)
.. _Vorbis: https://en.wikipedia.org/wiki/Vorbis

.. _AAC: https://en.wikipedia.org/wiki/Advanced_Audio_Coding
.. _HE-AAC: https://es.wikipedia.org/wiki/HE-AAC
.. _HE-AACv2: https://es.wikipedia.org/wiki/HE-AAC#HE-AAC_v2

.. _CBR: https://en.wikipedia.org/wiki/Constant_bitrate

.. _bookmarks:
.. _bookmark: https://en.wikipedia.org/wiki/Bookmark

.. _Affero GNU Public License v3: https://www.gnu.org/licenses/agpl-3.0.en.html

.. _FFmpeg: https://en.wikipedia.org/wiki/FFmpeg

.. _the greatest thing since sliced bread: https://en.wikipedia.org/wiki/Sliced_bread#In_popular_culture

This tool parses a Table of Contents file and:

- Optionally, shows HTML_ in your browser and print it too on the
  console, for copy&paste or redirection to complete your
  show notes.

- **TODO:** Optionally, adds the TOC generated HTML_ to an audio
  file.

- Optionally, adds timestamps (chapters) from your TOC file to
  an audio file.

- Optionally, adds timeoffsets to all timestamps (in the
  HTML_ and in the chapters) in order to compensate from initial
  presentation or teasers, advertisements during the audio, etc.

If the audio file already has chapter/TOC metadata, we will
replace it as requested. The rest of the metadata presents in the
original file will be preserved.

Install
-------

.. code-block:: console

     $ python3 -m pip install toc2audio

Command line
------------

.. code-block:: console

   $ toc2audio --version
   0.5.0

   $ toc2audio -h
   usage: toc2audio.py [-h] [--version] [--offset OFFSET] [--show]
                       [--toc] [--chapters]
                       [TOC] [AUDIO ...]

   Add Table of Contents and chapters to audio files

   positional arguments:
     TOC              Table of Contents file
     AUDIO            Audio file

   optional arguments:
     -h, --help       show this help message and exit
     --version        Show version info
     --offset OFFSET  Seconds or [HH:]MM:SS to add to ALL timestamps
     --show           Show the generated HTML in your browser
     --toc            Store Table of Contents in the audio file
     --chapters       Store chapters details in the audio file

Table of Contents format
------------------------

The Table of Contents must be written in markdown_.

toc2audio will parse any markdown_ file and will, optionally,
insert the generated HTML_ and chapters metadata in your audio
file. If you want to use timestamps (chapters), you must use lines
in this format:

[HH:MM:SS] Chapter title

HH:MM:SS is hours:minutes:seconds. The "hours" field is optional.
You can specify fields with one or two digits.

An example would be:

.. code-block:: text

   This audio was recorded blah blah...

   * [00:50] Presentation

       Here I describe the topics we will talk about.

   * [02:11] Topic 1

       Blah blah blah blah...

   * [17:29] Topic 2

       Blah blah blah blah...

.. note::

   Notice that when list items have multiple paragraphs, each
   subsequent paragrap **MUST BE indented** by either **FOUR**
   spaces or a tab, as documented in `Markdown Syntax
   Documentation
   <https://daringfireball.net/projects/markdown/syntax#list>`__
   and in the `documentation
   <https://python-markdown.github.io/#differences>`__ of
   `Python-Markdown <https://python-markdown.github.io/>`__
   project.

.. warning::

   If the first chapter doesn't start at "[00:00]" for whatever
   reason (including specifying a `Time offset`_), a dummy chapter
   will be implicitly added covering from "[00:00]" to the first
   chapter.

Time offset
-----------

You can apply a global time offset to all timestamps in the TOC
markdown_ document using the :code:`--offset` command line
parameter.

Supported audio containers
--------------------------

Supported audio containers are:

- Opus_. If you can choose an audio format freely, you should
  choose Opus_. It is the current (2021) state-of-art for general
  purpose audio (voice and music) and free of patents. It is
  "`the greatest thing since sliced bread`_".

- Vorbis_.

- MP3_.

  .. warning::

     In many MP3_ players, the MP3_ file **MUST BE** CBR_ in order
     for the chapter metadata seeking to be accurate.

- M4A_ (MP4_ audio).

  Usually, MP4_ audiobooks have a **m4b** extension to advertise
  the presence of bookmarks_. Nevertheless, the file is bitwise
  identical to **m4a**. Some software doesn't recognize **m4b**
  files, so I use a **m4a** suffix.

  Usually, the audio format will be AAC_, HE-AAC_ or HE-AACv2_,
  but I don't really care. I manipulate the generic MP4_
  container, I don't pay attention to the audio data. I guess I
  could even add chapters to video data.

  .. warning::

    This feature requires availability of FFmpeg_ software.

Author and License
------------------

The author of this package is Jesús Cea Avión.

- email: jcea@jcea.es.

- Webpage: https://www.jcea.es/.

- Blog: https://blog.jcea.es/.

- Twitter: `@jcea <https://twitter.com/jcea>`__.

- `Mercurial repository <https://hg.jcea.es/toc2audio/>`__.

This code is licensed under `Affero GNU Public License v3`_
(AGPLv3)



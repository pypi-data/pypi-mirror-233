Changelog
=========

.. include:: links.rst

* X.X.X - Work in progress

  - XX

* 1.1.1 - 2023-10-05

  - Migrate `pyproject.toml <https://peps.python.org/pep-0518/>`__
    metadata file to `PEP 621
    <https://peps.python.org/pep-0621>`__.

  - Some PEP8 fixes.

  - Python 3.12 is officially supported.

* 1.1.0 - 2022-05-17

  - **COMPATIBILITY WARNING:** Drop support for Python 3.6.

  - Add support for Python 3.10 and 3.11. Tested with 3.11.0b1.

  - Warnings in tests should be errors.

  - Migrate from 'unittest.makeSuite()' to
    'unittest.TestLoader.loadTestsFromTestCase()'.

  - More appropriate wording in the generated exception when the
    timestamps are not strictly monotonic.

  - Bibliography chapter.

  - Some typos in docs.

* 1.0.0 - 2021-05-18

  - When printing the chapter list in the terminal, show also the
    duration of the chapter in minutes and seconds.

  - When printing the chapter list in the terminal, align the
    titles of the chapters.

  - Add tutorial.

  - Production ready.

* 0.6.0 - 2021-04-20

  - Apparently, many players require that if chapters are present,
    they must cover all the audio.

    So, if the first chapter doesn't start at "[00:00]" because
    you don't specify it in the markdown_ TOC file or because you
    are applying a "timestamp offset", the software will generate
    a dummy chapter starting at "[00:00]".

  - MP3_: Chapter timestamps must be encoded as miliseconds, not
    seconds.

  - MP4_: Audio players require that the last chapter ends at the
    end of the audio file. If not, the player will keep playing
    "silence" until the end of the chapter.

  - MP3_: Just in case it is needed for audio players, last
    chapter ends at the end of the audio file.

  - MP4_: Missing :code:`import`.

* 0.5.0 - 2021-04-16

  - MP3_: Force a rewrite of the audio file only when the metadata
    is updated.

  - MP3_: Only clean old chapter information if we are adding new
    chapter information. Leave metadata alone if the user doesn't
    want to change it.

  - Add "toc2audio" identification in the audio file comment
    section.

  - MP4_: Preserve metadata of the original file, except the
    chapter information we are inserting.

  - Chapter titles: new lines transformed to spaces. Tabs
    transformed to spaces. Multiple spaces replaced by a single
    space.

  - When adding chapters to audio file, print the chapter list on
    the terminal.

  - **COMPATIBILITY WARNING:** Drop HTML tags in chapter titles.
    Keep only the text.

  - Better audio player chapter compatibility using Opus_ and
    Vorbis_ audio files.

* 0.4.0.post1 - 2021-04-14

  - Correct project URLs_ in PyPI_.

* 0.4.0 - 2021-04-14

  - **COMPATIBILITY WARNING:** Drop the feature of the first line
    in the markdown_ TOC file being the TOC title. Only MP3_
    supports that. Now, when tagging mp3_, we use the audio ID3_
    title as the TOC title.

  - Install :code:`toc2audio` command line utility.

  - Add :code:`--version` command line parameter.

  - New URLs_ for the project documentation, changelog, etc.

  - New theme for Sphinx: `sphinx_rtd_theme
    <https://github.com/readthedocs/sphinx_rtd_theme>`__.

* 0.3.0 - 2021-04-14

  - An optional :code:`--offset` command line parameter allows to
    specify a global offset to add to all timestamps. Useful to
    specify the duration of the intro you will add to the audio
    you listened in order to write the show notes markdown_
    document.

  - Beside showing the TOC in your browser, the HTML_ is printed
    in the terminal. You can copy&paste or redirect it to complete
    your show notes.

  - A timestamp can be shown as compact format (MM:SS) or not
    compact format (00:MM:SS).

  - A timestamp is declared as compact or not compact when read
    from the markdown_ TOC document. The idea is to keep the same
    representation that the user used in the markdown_ TOC
    document, after applying the optional time offsets.

* 0.2.0 - 2021-04-13

  - We can add chapters to M4A_ files now. This feature requires
    availability of FFmpeg_ software.

  - We can add chapters to Opus_ files now.

  - We can add chapters to Vorbis_ files now.

  - The chapter end time should be provided in the TOC object,
    instead of each audio tagger taking care of calculating it.

* 0.1.0 - 2021-04-09

  Initial release. It can add chapters to MP3_ files.

  .. warning::

     In many MP3_ players, the MP3_ file **MUST BE** CBR_ in order
     for the chapter metadata seeking to be accurate.

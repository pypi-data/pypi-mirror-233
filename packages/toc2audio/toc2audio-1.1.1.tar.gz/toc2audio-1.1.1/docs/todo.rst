To Do
-----

.. include:: links.rst

- 20220517 Being able to extract chapters from an audiofile.

- 20220517 Being able to extract TOC from audiofile.

- 20220517 Being able to embed TOC in an audiofile.

- 20220517 pypi page should be short and provide a BIG link to the
  real documentation.

- 20210525 Tests should run in a installed version of the package
  in a virtualenv.

- 20210520 Being able to HTML link a particular timestamp.

- 20210518 Customize HTML_ generation, CSS, etc.

- 20210421 MP3_ and possibly other audio file formats can insert
  images or URLs in chapters.

- 20210420 Write tests checking "ts_start > end of audio".

- 20210420 Implement custom exceptions.

- 20210420 Add a flag in the TOC object signaling the addition of
  the implicit chapter at the very beginning of the audio.

- 20210420 Being able to specify an image or URL for each chapter.

- 20210420 Being able to specify the name of the chapter at the
  very beginning of the audio, if the software creates it
  "implicitly".

- 20210416 We should be able to specify a fractional time offset.

- 20210415 When dumping the chapter list on the terminal, think
  about the convenience of dumping to stdout or stderr.

- 20210414 PyPI_ doesn't recognize :code:`:kbd:` in ReST_. I will
  use :code:`:code:`. for now.

- 20210413 Examples.

- 20210413 Being able to specify several time offsets in different
  positions, so we can compensate  advertisements or editions
  during the audio.

- 20210413 When specifying time offsets, we should be able to
  optionally specify a title. If present, it should be "inserted"
  in the TOC.

- 20210413 We could probably trivially support other Ogg_
  container based audio files.

- 20210413 TOC title for MP3_ files should be read from previous
  metadata present in the audio file, not from the Markdown. Other
  file formats have no TOC title.

- 20210413 M4A_ tagging requires FFMPEG_. Can we drop that
  dependency?

- 20210412 Manage correctly the presence of Markdown tags, links,
  "#", ";", "=", newline, etc in the chapter names.

- 20210411 Document that existing metadata not related to chapters
  or TOC, is not altered.

- 20210410 MP3_ VBR_: Parse the frames and provide byteoffset for
  the chapters. Would Players suppport it?

- 20210409 Being able to write timestamps in the markdown to tag
  sections without being added as chapters. For instance, using ()
  instead of [].

- 20210409 Tests should create temporal files in memory, not in
  the harddisk.

- 20210409 Publishing ReST_ to PyPI_ I lose "warnings" and "notes".

- 20210408 We don't know how long audio is, so we don't know how
  long is the last chapter. For now we asume "24 hours" and hope
  no audio player crashes.

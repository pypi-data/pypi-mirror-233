Obsidian Custom Exporter for `minchin.jrnl`
===========================================

This is an custom exporter for `minchin.jrnl
<http://minchin.ca/minchin.jrnl/>`_. The exported files are intended to be
loaded into `Obsidian <https://obsidian.md/>`_. In particular, metadata is
exported to the front matter format Obsidian understands and the body of the
entry is exported as is (but is generally assumed to be Markdown).

The exporter is installable from PyPI::

    pip install minchin.jrnl.contrib.exporter.obsidian

Please note that there are no safeties to ensure that exported files do not
overwrite existing files, or that two entries don't overwrite each other
during the export process.

Pull Requests to improve the functionality of this plugin are always
appreciated. As well, it may provide a helpful template if you want to write
your own custom exporter.

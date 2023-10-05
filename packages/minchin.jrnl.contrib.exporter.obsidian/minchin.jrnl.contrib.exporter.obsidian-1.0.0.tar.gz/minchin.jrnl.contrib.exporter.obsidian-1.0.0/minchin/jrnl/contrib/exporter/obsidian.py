from pathlib import Path
import re
import sys

from minchin.jrnl.color import ERROR_COLOR, RESET_COLOR, WARNING_COLOR
from minchin.jrnl.plugins.base import BaseExporter

__version__ = "1.0.0"


class Exporter(BaseExporter):
    """
    This Exporter can convert entries and journals into Markdown formatted text
    with YAML front matter.

    It is explicitly designed to produce source files for importing into `Obsidian
    <https://obsidian.md/>`_.
    """

    names = ["obsidian"]
    extension = "md"
    version = __version__

    @classmethod
    def export_entry(cls, entry, to_multifile=True):
        """Returns a markdown representation of a single entry, with YAML front matter."""
        if to_multifile is False:
            print(
                f"{ERROR_COLOR}ERROR{RESET_COLOR}: Obsidian export must be to \
                individual files. Please specify a directory to export to.",
                file=sys.stderr,
            )
            return

        date_str = entry.date.strftime(entry.journal.config["timeformat"])
        body_wrapper = "\n" if entry.body else ""
        body = body_wrapper + entry.body

        tagsymbols = entry.journal.config["tagsymbols"]
        # see also Entry.Entry.rag_regex
        multi_tag_regex = re.compile(rf"(?u)^\s*([{tagsymbols}][-+*#/\w]+\s*)+$")

        # # Increase heading levels in body text
        newbody = ""
        # heading = "#"
        previous_line = ""
        # warn_on_heading_level = False

        # TODO: check for double backslashes?
        first_line_flag = True

        for line in body.splitlines(True):
            # If the first line isn't a Level 1 heading, add the entry title as
            # a Level 1 heading
            if first_line_flag:
                first_line_flag = False
                if not re.match(r"^# ", line):
                    newbody = newbody + f"# {entry.title}\n"

            if False:
                pass
            #     if re.match(r"^#+ ", line):
            #         # ATX style headings
            #         newbody = newbody + previous_line + heading + line
            #         if re.match(r"^#######+ ", heading + line):
            #             warn_on_heading_level = True
            #         line = ""
            #     elif re.match(r"^=+$", line.rstrip()) and not re.match(
            #         r"^$", previous_line.strip()
            #     ):
            #         # Setext style H1
            #         newbody = newbody + heading + "# " + previous_line
            #         line = ""
            #     elif re.match(r"^-+$", line.rstrip()) and not re.match(
            #         r"^$", previous_line.strip()
            #     ):
            #         # Setext style H2
            #         newbody = newbody + heading + "## " + previous_line
            #         line = ""
            elif multi_tag_regex.match(line):
                # Tag only lines
                line = ""
            else:
                newbody = newbody + previous_line
            previous_line = line
        newbody = newbody + previous_line  # add very last line

        # # make sure the export ends with a blank line
        # if previous_line not in ["\r", "\n", "\r\n", "\n\r"]:
        #     newbody = newbody + os.linesep

        # if warn_on_heading_level is True:
        #     print(
        #         "{}WARNING{}: Headings increased past H6 on export - {} {}".format(
        #             WARNING_COLOR, RESET_COLOR, date_str, entry.title
        #         ),
        #         file=sys.stderr,
        #     )

        dayone_attributes = ""
        if hasattr(entry, "uuid"):
            dayone_attributes += "uuid: " + entry.uuid + "\n"

        # Obsidian properties can't be nested
        if hasattr(entry, "creator_device_agent"):
            dayone_attributes += f"creator/device agent: {entry.creator_device_agent}\n"
        if hasattr(entry, "creator_generation_date"):
            dayone_attributes += "creator/generation date: {}\n".format(
                str(entry.creator_generation_date)
            )
        if hasattr(entry, "creator_host_name"):
            dayone_attributes += f"creator/host name: {entry.creator_host_name}\n"
        if hasattr(entry, "creator_os_agent"):
            dayone_attributes += f"creator/os agent: {entry.creator_os_agent}\n"
        if hasattr(entry, "creator_software_agent"):
            dayone_attributes += (
                f"creator/software agent: {entry.creator_software_agent}\n"
            )

        # TODO: copy over pictures, if present
        # source directory is  entry.journal.config['journal']
        # output directory is...?

        return "{frontmatter_start}title: {title}\ndate: {date}\nstarred: {starred}\ntags: {tags}\n{dayone}{frontmatter_end}{body}{space}".format(
            date=date_str,
            title=entry.title,
            starred=entry.starred,
            tags=", ".join([tag[1:] for tag in entry.tags]),
            dayone=dayone_attributes,
            body=newbody,
            space="\n",
            frontmatter_start="---\n",
            frontmatter_end="---\n\n",
        )

    @classmethod
    def export_journal(cls, journal):
        """Returns an error, as Obsidian export requires a directory as a target."""
        # minchin.jrnl prints the error message
        raise NotImplementedError

    @classmethod
    def make_filename(cls, entry):
        """Determine the filename to save an individual entry as."""
        if hasattr(entry, "uuid"):
            # DayOne journals allowed a single entry per day
            # Daily notes format
            fn = (
                Path(entry.date.strftime("%Y"))
                / entry.date.strftime("%m")
                / entry.date.strftime("%d")
            )

            # # Weekly Notes format
            # fn = (
            #     Path(entry.date.strftime("%G"))
            #     / entry.date.strftime("%G-W%W")
            # )

            # # zettel format
            # # does assume that no two entries are at the same time
            # fn = Path(entry.date.strftime("%Y%m%D%H%M"))
            # print(fn)

            fn = fn.with_suffix("." + cls.extension)
            return fn

        else:
            # zettel format
            # does assume that no two entries are at the same time
            fn = Path(entry.date.strftime("%Y%m%d%H%M"))

            fn = fn.with_suffix("." + cls.extension)
            return fn
            # return super().make_filename(entry)
        # return entry.date.strftime("%Y-%m-%d") + "_{}.{}".format(
        #     cls._slugify(str(entry.title)), cls.extension
        # )

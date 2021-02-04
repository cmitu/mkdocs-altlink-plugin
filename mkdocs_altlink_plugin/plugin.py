import re
import os

from textwrap import dedent

from mkdocs.config import Config
from mkdocs.plugins import BasePlugin

class AlternateLinkPlugin(BasePlugin):

    MD_LINK_RE = re.compile(r']\(([^)]*)\)', re.UNICODE)
    FENCED_BLOCK_RE = re.compile(
        dedent(r'''
            (?P<fence>^(?:~{3,}|`{3,}))[ ]*                      # opening fence
            ((\{(?P<attrs>[^\}\n]*)\})?|                         # (optional {attrs} or
            (\.?(?P<lang>[\w#.+-]*))?[ ]*                        # optional (.)lang
            (hl_lines=(?P<quot>"|')(?P<hl_lines>.*?)(?P=quot))?) # optional hl_lines)
            [ ]*\n                                               # newline (end of opening fence)
            (?P<code>.*?)(?<=\n)                                 # the code block
            (?P=fence)[ ]*$                                      # closing fence
        '''),
        re.MULTILINE | re.DOTALL | re.VERBOSE
    )


    def _should_ignore_link(self, link):
        return link.startswith(u"http") or link.startswith(u"#") or link.startswith(u"ftp") or link.startswith(u"www") or link.startswith(u"mailto") or link.endswith(u".md")

    def _is_valid_file(self, path, root):
        return os.path.exists(path) or os.path.exists(root + "/" + path)

    def on_page_markdown(self, markdown, page = None, config = None, **kwargs):

        doc_dir = config.data.get("docs_dir")

        # Get the list of code blocks present in the document
        code_blocks = re.finditer(self.FENCED_BLOCK_RE, markdown)

        offset = 0
        out_markdown = markdown
        for m in re.finditer(self.MD_LINK_RE, markdown):
            is_fenced = False
            link = m.string[m.start(1):m.end(1)]

            if self._should_ignore_link(link.lstrip()):
                continue

            # Get any anchors in the URL
            vals = link.lstrip().split("#")

            # Check if it's a valid internal .md page URL
            if vals[0].endswith(".md"):
                continue

            # Check if the link is not part of a code block
            for block in code_blocks:
                if block.start() < m.start(1) and block.end() >= m.start(1):
                    is_fenced = True
                    break
            if is_fenced:
                continue

            # Check if the link is not a resource linked (img/pdf/etc)
            if self._is_valid_file(vals[0], doc_dir):
                continue

            # Append .md to the page name, this is an internal link candidate
            vals[0] += ".md"

            # Re-construct the link
            href_new = "#".join(vals)

            # Replace the values in the markdown
            out_markdown = out_markdown[:m.start(1) + offset] + href_new + out_markdown[m.end(1) + offset:]

            # Offset the matches with the replaced value's length
            offset += len(href_new) - (m.end(1) - m.start(1))

        return out_markdown

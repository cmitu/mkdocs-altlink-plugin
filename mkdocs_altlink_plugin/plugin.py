import re
import os

from mkdocs.config import Config
from mkdocs.plugins import BasePlugin

class AlternateLinkPlugin(BasePlugin):

    MD_LINK = re.compile(r']\(([^)]*)\)', re.UNICODE)

    def _should_ignore_link(self, link):
        return link.startswith(u"http") or link.startswith(u"#") or link.startswith(u"ftp") or link.startswith(u"www") or link.startswith(u"mailto") or link.endswith(u".md")

    def _is_valid_file(self, path, root):
        return os.path.exists(path) or os.path.exists(root + "/" + path)

    def on_page_markdown(self, markdown, page = None, config = None, **kwargs):

        links = re.findall(self.MD_LINK, markdown)
        doc_dir = config.data.get("docs_dir")

        for link in links:
            if self._should_ignore_link(link.lstrip()):
                continue

            # Get any anchors in the URL
            vals = link.lstrip().split("#")

            # Check if it's a valid internal .md page URL
            if vals[0].endswith(".md"):
                continue

            # Check if the link is not a resource linked (img/pdf/etc)
            if self._is_valid_file(vals[0], doc_dir):
                continue

            # Append .md to the page name,this is an internal link candidate
            vals[0] += ".md"

            # Re-construct the link
            href_new = "#".join(vals)

            # Replace the values in the markdown
            markdown = markdown.replace("({})".format(link), "({})".format(href_new))

        return markdown

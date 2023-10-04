"""
An editor for your website.

Implements a Micropub editor.

"""

import json
import pprint

import sqlyte
import web
import webagt

app = web.application(__name__, prefix="editor")


@app.control("")
class Drafts:
    """All Drafts."""

    def get(self):
        """Return a list of all drafts."""
        return app.view.drafts()

    def post(self):
        return
        # form = web.form("content")
        # web.application("understory.posts").model.create(
        #     "entry", {"content": form.content}
        # )
        # return "entry created"


@app.control("draft")
class Draft:
    """A draft."""

    def get(self):
        """Return the draft."""
        permalink = web.form(permalink=None).permalink
        post = {}
        if permalink:
            post = web.application("webint_posts").model.read(permalink)["resource"]
        else:
            permalink, _ = web.application("webint_posts").model.create("entry")
            raise web.SeeOther(f"/editor/draft?permalink={permalink}")
        return app.view.draft(
            post,
            web.application("webint_owner").model.get_identities(),
            [],  # web.application("webint_guests").model.get_guests(),
        )

    def post(self):
        return
        # form = web.form("content")
        # web.application("understory.posts").model.create(
        #     "entry", {"content": form.content}
        # )
        # return "entry created"


@app.control("preview/markdown")
class PreviewMarkdown:
    """"""

    def get(self):
        return (
            "<form method=post>"
            "<textarea name=content></textarea>"
            "<button>Preview</button>"
            "</form>"
        )

    def post(self):
        form = web.form("pad_id", context=None)
        etherpad_content = sqlyte.db(
            "/home/admin/app/run/media/pads/etherpad-lite/var/sqlite.db"
        ).select("store", where="key = ?", vals=[f"pad:{form.pad_id}"])[0]["value"]
        content = json.loads(etherpad_content)["atext"]["text"]
        rendered = str(
            web.mkdn(
                str(
                    web.template(
                        content,
                        globals={"get": webagt.get, "pformat": pprint.pformat},
                        restricted=True,
                    )()
                ),
                form.context,
            )  # , globals=micropub.markdown_globals)
        )
        web.header("Content-Type", "application/json")
        return {
            "content": rendered,
            # "readability": micropub.readability.Readability(form.content).metrics,
        }


@app.control("preview/resource")
class PreviewResource:
    """"""

    def get(self):
        url = web.form(url=None).url
        web.header("Content-Type", "application/json")
        if not url:
            return {}
        resource = web.get(url)
        if resource.entry.data:
            return resource.entry
        if resource.event.data:
            return resource.event
        if resource.feed.data:
            return resource.feed
        return {}

        # XXX data = cache.parse(url)
        # XXX if "license" in data["data"]["rels"]:
        # XXX     data["license"] = data["data"]["rels"]["license"][0]
        # XXX try:
        # XXX     edit_page = data["html"].cssselect("#ca-viewsource a")[0]
        # XXX except IndexError:
        # XXX     # h = html2text.HTML2Text()
        # XXX     # try:
        # XXX     #     data["content"] = h.handle(data["entry"]["content"]).strip()
        # XXX     # except KeyError:
        # XXX     #     pass
        # XXX     try:
        # XXX         markdown_input = ("html", data["entry"]["content"])
        # XXX     except (KeyError, TypeError):
        # XXX         markdown_input = None
        # XXX else:
        # XXX     edit_url = web.uri.parse(str(data["url"]))
        # XXX     edit_url.path = edit_page.attrib["href"]
        # XXX     edit_page = fromstring(requests.get(edit_url).text)
        # XXX     data["mediawiki"] = edit_page.cssselect("#wpTextbox1")[0].value
        # XXX     data["mediawiki"] = (
        # XXX         data["mediawiki"].replace("{{", r"{!{").replace("}}", r"}!}")
        # XXX     )
        # XXX     markdown_input = ("mediawiki", data["mediawiki"])

        # XXX if markdown_input:
        # XXX     markdown = str(
        # XXX         sh.pandoc(
        # XXX         "-f", markdown_input[0], "-t", "markdown", _in=markdown_input[1]
        # XXX         )
        # XXX     )
        # XXX     for n in range(1, 5):
        # XXX         indent = "    " * n
        # XXX         markdown = markdown.replace(f"\n{indent}-",
        # XXX                                     f"\n{indent}\n{indent}-")
        # XXX     markdown = re.sub(r'\[(\w+)\]\(\w+ "wikilink"\)', r"[[\1]]", markdown)
        # XXX     markdown = markdown.replace("–", "--")
        # XXX     markdown = markdown.replace("—", "---")
        # XXX     data["content"] = markdown

        # XXX data.pop("html")
        # XXX # XXX data["category"] = list(set(data["entry"].get("category", [])))
        # XXX web.header("Content-Type", "application/json")
        # XXX return dump_json(data)

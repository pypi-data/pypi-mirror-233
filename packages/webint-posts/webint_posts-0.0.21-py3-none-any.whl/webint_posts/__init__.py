"""
Manage posts on your website.

Implements a Micropub server.

"""

import random

import mf

# import micropub
import web
import webagt
import webint_media
import webint_search

# import webmention
# import websub


class PostAccessError(Exception):
    """Post could not be access."""


class PostNotFoundError(Exception):
    """Post could not be found."""


app = web.application(
    __name__,
    prefix="posts",
    args={
        "channel": r".+",
        "entry": r".+",
        "year": r"\d{4}",
        "month": r"\d{2}",
        "day": r"\d{2}",
        "post": web.nb60_re + r"{,4}",
        "slug": r"[\w_-]+",
        "page": r"[\w-]+",
    },
    model={
        "resources": {
            "permalink": "TEXT UNIQUE",
            "version": "TEXT UNIQUE",
            "resource": "JSON",
        },
        "deleted_resources": {
            "permalink": "TEXT",
            "version": "TEXT UNIQUE",
            "resource": "JSON",
        },
        "syndication": {"destination": "JSON NOT NULL"},
    },
)

# TODO supported_types = {"RSVP": ["in-reply-to", "rsvp"]}


def get_config():
    """"""
    syndication_endpoints = []
    # TODO "channels": generate_channels()}
    return {
        "q": ["category", "contact", "source", "syndicate-to"],
        "media-endpoint": f"{web.tx.origin}/media",
        "syndicate-to": syndication_endpoints,
        "visibility": ["public", "unlisted", "private"],
        "timezone": "America/Los_Angeles",
    }


def generate_trailer():
    letterspace = "abcdefghijkmnopqrstuvwxyz23456789"
    trailer = "".join([random.choice(letterspace) for i in range(2)])
    if trailer in ("bs", "ok", "hi", "oz", "lb"):
        return generate_trailer()
    else:
        return trailer


@app.wrap
def linkify_head(handler, main_app):
    """."""
    yield
    if web.tx.request.uri.path == "":
        web.add_rel_links(micropub="/posts")


def route_unrouted(handler, app):  # TODO XXX ???
    """Handle channels."""
    for channel in app.model.get_channels():
        if channel["resource"]["url"][0] == f"/{web.tx.request.uri.path}":
            posts = app.model.get_posts_by_channel(channel["resource"]["uid"][0])
            web.header("Content-Type", "text/html")
            raise web.OK(app.view.channel(channel, posts))
    yield


@app.control("")
class MicropubEndpoint:
    """Your posts."""

    def get(self):
        """"""
        try:
            form = web.form("q")
        except web.BadRequest:
            return app.view.activity(
                app.model.get_channels(),
                [],  # TODO web.application("webint_media").model.get_media(),
                app.model.get_posts(),
            )

        def generate_channels():
            return [
                {"name": r["name"][0], "uid": r["uid"][0]}
                for r in app.model.get_channels()
            ]

        # TODO XXX elif form.q == "channel":
        # TODO XXX     response = {"channels": generate_channels()}
        if form.q == "config":
            response = get_config()
        elif form.q == "source":
            response = {}
            if "search" in form:
                response = {
                    "items": [
                        {"url": [r["resource"]["url"]]}
                        for r in app.model.search(form.search)
                    ]
                }
            elif "url" in form:
                response = dict(app.model.read(form.url))
            else:
                pass  # TODO list all posts
        elif form.q == "category":
            response = {"categories": app.model.get_categories()}
        else:
            raise web.BadRequest("unsupported query. check `q=config` for support.")
        web.header("Content-Type", "application/json")
        return response

    def post(self):
        """"""
        # TODO check for bearer token or session cookie
        # try:
        #     payload = web.form("h")
        # except web.BadRequest:
        post_type = None
        properties = {}
        if str(web.tx.request.headers["content-type"]) == "application/json":
            payload = web.tx.request.body._data
            if "action" not in payload:
                properties = payload["properties"]
                post_type = payload.pop("type")[0].split("-")[1]
        else:
            payload = web.form()
            post_type = payload.pop("h", None)
        # else:  # form-encoded update/delete
        #     properties = payload
        # else:  # form-encoded create
        #     post_type = payload.pop("h")
        #     properties = payload
        action = payload.pop("action", "create")
        if not properties:
            properties = dict(payload)

        if not web.tx.user.is_owner:
            try:
                token = properties.pop("access_token")[0]
            except KeyError:
                token = str(web.tx.request.headers["authorization"])
            auth = web.application("webint_auth").model.get_auth_from_token(token)
            properties["token"] = auth["auth_id"]

        def collect_properties(properties):
            props = {}
            for k, v in properties.items():
                k = k.rstrip("[]")
                if not isinstance(v, list):
                    v = [v]
                if k == "content" and not isinstance(v[0], dict):
                    v[0] = {"html": v[0]}
                if not v[0]:
                    continue
                props[k] = v
            return props

        mentions = []
        permalink = payload.pop("url", None)
        # syndication = []
        if action == "create":
            permalink, mentions = app.model.create(
                post_type, **collect_properties(properties)
            )
            # syndication = properties.get("syndication")
            # web.header("Link", '</blat>; rel="shortlink"', add=True)
            # web.header("Link", '<https://twitter.com/angelogladding/status/'
            #                    '30493490238590234>; rel="syndication"', add=True)

            # XXX web.braid(permalink, ...)

            # TODO web.enqueue(
            # TODO     websub.publish,
            # TODO     f"{web.tx.origin}/subscriptions",
            # TODO     f"{web.tx.origin}",
            # TODO     str(content.Homepage().get()),
            # TODO )
        elif action == "update":
            if "add" in payload:
                app.model.update(permalink, add=collect_properties(payload["add"]))
                # syndication = payload["add"]["syndication"]
            if "replace" in payload:
                app.model.update(
                    permalink, replace=collect_properties(payload["replace"])
                )
                # syndication = payload["replace"]["syndication"]
        elif action == "delete":
            app.model.delete(permalink)
        else:
            return f"ACTION `{action}` NOT IMPLEMENTED"
        # XXX if "mastodon" in syndication:
        # XXX     mentions.append("https://fed.brid.gy")
        for mention in mentions:
            web.application("webint_mentions").model.send_mention(permalink, mention)
        if action == "create":
            raise web.Created(f"post created at: {permalink}", permalink)


@app.control("channels")
class Channels:
    """Your channels."""

    def get(self):
        """"""
        return app.view.channels(app.model.get_channels())


@app.control("channels/{channel}")
class Channel:
    """A single channel."""

    def get(self):
        """"""
        return app.view.channel(self.channel)


@app.control("syndication")
class Syndication:
    """Your syndication destinations."""

    def get(self):
        """"""
        return app.view.syndication()

    def post(self):
        """"""
        destinations = web.form()
        if "twitter_username" in destinations:
            un = destinations.twitter_username
            # TODO pw = destinations.twitter_password
            # TODO sign in
            user_photo = ""  # TODO doc.qS(f"a[href=/{un}/photo] img").src
            destination = {
                "uid": f"//twitter.com/{un}",
                "name": f"{un} on Twitter",
                "service": {
                    "name": "Twitter",
                    "url": "//twitter.com",
                    "photo": "//abs.twimg.com/favicons/" "twitter.ico",
                },
                "user": {"name": un, "url": f"//twitter.com/{un}", "photo": user_photo},
            }
            web.tx.db.insert("syndication", destination=destination)
        if "github_username" in destinations:
            un = destinations.github_username
            # TODO token = destinations.github_token
            # TODO check the token
            user_photo = ""  # TODO doc.qS("img.avatar-user.width-full").src
            destination = {
                "uid": f"//github.com/{un}",
                "name": f"{un} on GitHub",
                "service": {
                    "name": "GitHub",
                    "url": "//github.com",
                    "photo": "//github.githubassets.com/" "favicons/favicon.png",
                },
                "user": {"name": un, "url": f"//github.com/{un}", "photo": user_photo},
            }
            web.tx.db.insert("syndication", destination=destination)


@app.control("{year}", prefixed=False)
class Year:
    """Posts for a given year."""

    def get(self, year):
        """Render a chronological list of posts for the given year."""
        year = int(year)
        return app.view.year(
            year,
            app.model.get_posts(after=f"{year-1}-12-31", before=f"{year+1}-01-01"),
        )


@app.control("{year}/{month}", prefixed=False)
class Month:
    """Posts for a given month."""

    def get(self, year, month):
        """Render a chronological list of posts for the given month."""
        year = int(year)
        month = int(month)
        return app.view.month(
            year,
            month,
            app.model.get_posts(
                after=f"{year-1}-{month-1:02}-31", before=f"{year+1}-{month:02}-01"
            ),
        )


@app.control("{year}/{month}/{day}", prefixed=False)
class Day:
    """Posts for a given day."""

    def get(self, year, month, day):
        """Render a chronological list of posts for the given day."""
        year = int(year)
        month = int(month)
        day = int(day)
        return app.view.day(
            year,
            month,
            day,
            app.model.get_posts(
                after=f"{year-1}-{month-1:02}-{day-1:02}",
                before=f"{year+1}-{month:02}-{day:02}",
            ),
        )


@app.control(r"{year}/{month}/{day}/{post}(/{slug})?|{page}", prefixed=False)
class Permalink:
    """An individual entry."""

    def get(self, year=None, month=None, day=None, post=None, slug=None, page=None):
        """Render a page."""
        try:
            resource = app.model.read(web.tx.request.uri.path)["resource"]
        except PostNotFoundError as err:
            web.header("Content-Type", "text/html")  # TODO FIXME XXX
            raise web.NotFound(app.view.entry_not_found(err))
        except PostAccessError as err:
            web.header("Content-Type", "text/html")  # TODO FIXME XXX
            raise web.NotFound(app.view.access_denied(err))
        if resource["visibility"] == "private" and not web.tx.user.session:
            raise web.Unauthorized(f"/auth?return_to={web.tx.request.uri.path}")
        mentions = web.application(
            "webint_mentions"
        ).model.get_received_mentions_by_target(
            f"{web.tx.origin}/{web.tx.request.uri.path}"
        )
        if page:
            permalink = f"/{page}"
        else:
            permalink = f"/{year}/{month}/{day}/{post}"
        return app.view.entry(permalink, resource, mentions)


@app.query
def create(db, resource_type, **resource):
    """Create a resource."""
    for k, v in resource.items():
        if not isinstance(v, list):
            resource[k] = [v]
        flat_values = []
        for v in resource[k]:
            if isinstance(v, dict):
                if not ("html" in v or "datetime" in v):
                    v = dict(**v["properties"], type=[v["type"][0].removeprefix("h-")])
            flat_values.append(v)
        resource[k] = flat_values

    config = get_config()
    # TODO deal with `updated`/`drafted`?
    if "published" in resource:
        # TODO accept simple eg. published=2020-2-20, published=2020-2-20T02:22:22
        # XXX resource["published"][0]["datetime"] = pendulum.from_format(
        # XXX     resource["published"][0]["datetime"], "YYYY-MM-DDTHH:mm:ssZ"
        # XXX )
        # XXX published = resource["published"]
        pass
    else:
        resource["published"] = [
            {
                "datetime": web.now().isoformat(),
                "timezone": config["timezone"],
            }
        ]
    published = web.parse_dt(
        resource["published"][0]["datetime"],
        tz=resource["published"][0]["timezone"],
    )

    resource["visibility"] = resource.get("visibility", ["private"])
    if "audience" in resource:
        resource["visibility"] = ["protected"]
    # XXX resource["channel"] = resource.get("channel", [])
    mentions = []
    urls = resource.pop("url", [])
    # if resource_type == "card":
    #     slug = resource.get("nickname", resource.get("name"))[0]
    # elif resource_type == "event":
    #     slug = resource.get("nickname", resource.get("name"))[0]
    #     urls.insert(0, f"/pub/cards/{web.textslug(slug)}")
    #     # if resource["uid"] == str(web.uri(web.tx.host.name)):
    #     #     pass
    #     urls.insert(0, f"/pub/cards/{web.textslug(slug)}")
    # elif resource_type == "feed":
    #     name_slug = web.textslug(resource["name"][0])
    #     try:
    #         slug = resource["slug"][0]
    #     except KeyError:
    #         slug = name_slug
    #     resource.update(uid=[slug if slug else name_slug])
    #     resource.pop("channel", None)
    #     # XXX urls.insert(0, f"/{slug}")
    permalink = None
    if resource_type == "ragt-ag-project":
        name = resource["name"][0]
        permalink = f"/code/{name}"
        urls.insert(0, permalink)
        resource.update(url=urls, type=[resource_type])
        web.application("webint_code").model.create_project(name)
        db.insert(
            "resources",
            permalink=permalink,
            version=web.nbrandom(10),
            resource=resource,
        )
    elif resource_type == "entry":
        #                                         REQUEST URL
        # 1) given: url=/xyz                        => look for exact match
        #     then: url=[/xyz, /2021/3/5...]
        # 2) given: channel=abc, slug=foo           => construct
        #     then: url=[/2021/3/5...]
        # 3) given: no slug                         => only via permalink
        #     then: url=[/2021/3/5...]
        post_type = mf.discover_post_type(resource)
        slug = None
        if post_type == "article":
            slug = resource["name"][0]
        elif post_type == "listen":
            result = webint_search.search_youtube(resource["listen-of"][0])[0]["id"]
            web.enqueue(webint_media.download, f"https://youtube.com/watch?v={result}")
        elif post_type == "bookmark":
            mentions.append(resource["bookmark-of"][0])
        elif post_type == "like":
            mentions.append(resource["like-of"][0])
        elif post_type == "rsvp":
            event_url = resource["in-reply-to"][0]
            if event_url.startswith("calshow:"):
                event_url = event_url.partition("\n")[2]
            mentions.append(event_url)
            resource["in-reply-to"][0] = event_url
        # elif post_type == "identification":
        #     identifications = resource["identification-of"]
        #     identifications[0] = {"type": "cite",
        #                           **identifications[0]["properties"]}
        #     textslug = identifications[0]["name"]
        #     mentions.append(identifications[0]["url"])
        # elif post_type == "follow":
        #     follows = resource["follow-of"]
        #     follows[0] = {"type": "cite", **follows[0]["properties"]}
        #     textslug = follows[0]["name"]
        #     mentions.append(follows[0]["url"])
        #     web.tx.sub.follow(follows[0]["url"])
        # TODO user indieauth.server.get_identity() ??
        # XXX author_id = list(db.select("identities"))[0]["card"]
        # XXX author_id = get_card()db.select("resources")[0]["card"]["version"]
        resource.update(author=[web.tx.origin])

        resource.update(url=urls, type=[resource_type])
        permalink_base = f"/{web.timeslug(published)}"
        while True:
            permalink = f"{permalink_base}/{generate_trailer()}"
            resource["url"].append(permalink)
            try:
                db.insert(
                    "resources",
                    permalink=permalink,
                    version=web.nbrandom(10),
                    resource=resource,
                )
            except db.IntegrityError:
                continue
            break
    return permalink, mentions


@app.query
def read(db, url):
    """Return an entry with its metadata."""
    if not url.startswith(("http://", "https://")):
        url = f"/{url.strip('/')}"
    try:
        resource = db.select(
            "resources",
            where="""json_extract(resources.resource, '$.url[0]') == ?""",
            vals=[url],
        )[0]
    except IndexError:
        try:
            resource = db.select(
                "resources",
                where="""json_extract(resources.resource, '$.url[1]') == ?""",
                vals=[url],
            )[0]
        except IndexError:
            raise PostNotFoundError(url)
    r = resource["resource"]
    if r["visibility"][0] == "private" and not web.tx.user.is_owner:
        raise PostAccessError("Owner only")
    if r["visibility"][0] == "protected" and not web.tx.user.is_owner:
        uid = web.tx.user.session.get("uid", [None])
        if uid[0] not in r.get("audience", []):
            raise PostAccessError("No access")
    if "entry" in r["type"]:
        # XXX r["author"] = web.tx.identities.get_identity(r["author"][0])["card"]
        r["author"] = [web.application("webint_owner").model.get_identity("/")["card"]]
    return resource


@app.query
def update(db, url, add=None, replace=None, remove=None):
    """Update a resource."""
    if url.startswith(("http://", "https://")):
        url = webagt.uri(url).path
    else:
        url = url.strip("/")
    permalink = f"/{url}"
    resource = db.select("resources", where="permalink = ?", vals=[permalink])[0][
        "resource"
    ]
    if add:
        for prop, vals in add.items():
            try:
                resource[prop].extend(vals)
            except KeyError:
                resource[prop] = vals
    if replace:
        for prop, vals in replace.items():
            resource[prop] = vals
    if remove:
        for prop, vals in remove.items():
            del resource[prop]
    resource["updated"] = [web.now().in_timezone("America/Los_Angeles")]
    resource = web.load(web.dump(resource))
    db.update("resources", resource=resource, where="permalink = ?", vals=[permalink])
    # TODO web.publish(url, f".{prop}[-0:-0]", vals)


@app.query
def delete(db, url):
    """Delete a resource."""
    # XXX resource = app.model.read(url)
    with db.transaction as cur:
        # XXX cur.insert("deleted_resources", **resource)
        cur.delete("resources", where="permalink = ?", vals=[url])


@app.query
def search(db, query):
    """Return a list of resources containing `query`."""
    where = """json_extract(resources.resource,
                   '$.bookmark-of[0].url') == ?
               OR json_extract(resources.resource,
                   '$.like-of[0].url') == ?"""
    return db.select("resources", vals=[query, query], where=where)


@app.query
def get_identity(db, version):
    """Return a snapshot of an identity at given version."""
    return app.model.get_version(version)


@app.query
def get_version(db, version):
    """Return a snapshot of resource at given version."""
    return db.select("resources", where="version = ?", vals=[version])[0]


@app.query
def get_entry(db, path):
    """"""


@app.query
def get_card(db, nickname):
    """Return the card with given nickname."""
    resource = db.select(
        "resources",
        vals=[nickname],
        where="""json_extract(resources.resource,
                                         '$.nickname[0]') == ?""",
    )[0]
    return resource["resource"]


@app.query
def get_event(db, path):
    """"""


@app.query
def get_entries(db, limit=20, modified="DESC"):
    """Return a list of entries."""
    return db.select(
        "resources",
        order=f"""json_extract(resources.resource,
                                      '$.published[0]') {modified}""",
        where="""json_extract(resources.resource,
                                     '$.type[0]') == 'entry'""",
        limit=limit,
    )


@app.query
def get_cards(db, limit=20):
    """Return a list of alphabetical cards."""
    return db.select(
        "resources",  # order="modified DESC",
        where="""json_extract(resources.resource,
                                     '$.type[0]') == 'card'""",
    )


@app.query
def get_rooms(db, limit=20):
    """Return a list of alphabetical rooms."""
    return db.select(
        "resources",  # order="modified DESC",
        where="""json_extract(resources.resource,
                                     '$.type[0]') == 'room'""",
    )


@app.query
def get_channels(db):
    """Return a list of alphabetical channels."""
    return db.select(
        "resources",  # order="modified DESC",
        where="json_extract(resources.resource, '$.type[0]') == 'feed'",
    )


@app.query
def get_categories(db):
    """Return a list of categories."""
    return [
        r["value"]
        for r in db.select(
            "resources, json_each(resources.resource, '$.category')",
            what="DISTINCT value",
        )
    ]


@app.query
def get_posts(db, after=None, before=None, categories=None):
    """."""
    froms = ["resources"]
    wheres = ""
    vals = []

    # by visibility
    vis_sql = "json_extract(resources.resource, '$.visibility[0]')"
    vis_wheres = [f"{vis_sql} == 'public'"]
    if web.tx.user.session:
        vis_wheres.append(f"{vis_sql} == 'protected'")
    if web.tx.user.is_owner:
        vis_wheres.append(f"{vis_sql} == 'private'")
    wheres += "(" + " OR ".join(vis_wheres) + ")"

    # by date
    dt_wheres = []
    dt_vals = []
    if after:
        dt_wheres.append(
            "dttz_to_iso(json_extract(resources.resource, '$.published[0]')) > ?"
        )
        dt_vals.append(after)
    if before:
        dt_wheres.append(
            "dttz_to_iso(json_extract(resources.resource, '$.published[0]')) < ?"
        )
        dt_vals.append(before)
    if before or after:
        wheres += " AND (" + " AND ".join(dt_wheres) + ")"
        vals.extend(dt_vals)

    # by category
    if categories:
        cat_wheres = []
        cat_vals = []
        for n, category in enumerate(categories):
            froms.append(f"json_each(resources.resource, '$.category') as v{n}")
            cat_wheres.append(f"v{n}.value = ?")
            cat_vals.append(category)
        wheres += " AND (" + " AND ".join(cat_wheres) + ")"
        vals.extend(cat_vals)

    for post in db.select(
        ", ".join(froms),
        where=wheres,
        vals=vals,
        order="""json_extract(resources.resource, '$.published[0]') DESC""",
    ):
        r = post["resource"]
        if (
            r["visibility"][0] == "protected"
            and not web.tx.user.is_owner
            and web.tx.user.session["uid"][0] not in r["audience"]
        ):
            continue
        if "entry" in r["type"]:
            r["author"] = [
                web.application("webint_owner").model.get_identity("/")["card"]
            ]
        yield r


@app.query
def get_posts_by_channel(db, uid):
    """."""
    return db.select(
        "resources",
        vals=[uid],
        where="""json_extract(resources.resource, '$.channel[0]') == ?""",
        order="""json_extract(resources.resource, '$.published[0]') DESC""",
    )


# def get_channels(db):
#     """Return a list of channels."""
#     return [r["value"] for r in
#             db.select("""resources,
#                            json_tree(resources.resource, '$.channel')""",
#                          what="DISTINCT value", where="type = 'text'")]


@app.query
def get_year(db, year):
    return db.select(
        "resources",
        order="""json_extract(resources.resource,
                                     '$.published[0].datetime') ASC""",
        where=f"""json_extract(resources.resource,
                                      '$.published[0].datetime')
                                      LIKE '{year}%'""",
    )

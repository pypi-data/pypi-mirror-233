import aiohttp
from .mastodon import MastodonApplication
from .firefish import FirefishApplication


async def activity_for_mastodon(
    domain: str, username: str, access_token: str, session: aiohttp.ClientSession
):
    """Creates a ApplicationAdapterForLastActivity object for connecting to
    mastodon. Example usage:

    ```python
    mastodon = await activity_for_mastodon("mastodon_web", "bob", "xxx", session)
    ```
    """
    mastodon = MastodonApplication(
        domain=domain, access_token=access_token, username=username
    )

    return mastodon.last_activity(session)


async def activity_for_firefish(
    domain: str, username: str, session: aiohttp.ClientSession
):
    """Creates a ApplicationAdapterForLastActivity object for connecting to
    firefish. Example usage:

    ```python
    firefish = await activity_for_firefish("firefish_web", "admin", session)
    ```
    """
    firefish = FirefishApplication(domain=domain, username=username)

    return await firefish.last_activity(session)

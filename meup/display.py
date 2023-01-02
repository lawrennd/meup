from IPython.display import display, HTML

from . import access


def link(link, label=None, description=None):
    """Display a link and a label"""
    if label is None:
        label = link
    html = f"<a href='{link}' target='_blank'>{label}</a>"
    if description is not None:
        html += f"<p>{description}</p>"
    display(HTML(html))


def useful_links():
    """Display the list of useful links"""
    for useful in access.config["useful_links"]:    
        link(**useful)

def tweets(tweets):
    """Display tweets to an Jupyter notebook"""
    for index, tweet in tweets.iterrows():
        tweetid = index
        text = tweet["text"]
        name = tweet["name"]
        username = tweet["username"]
        link(link=f"https://twitter.com/{username}",
             label=name)
        link(link=f"https://twitter.com/i/web/status/{tweetid}",
             label=tweetid,
             description=text)     



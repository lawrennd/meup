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
    for tweet in tweets.data:
        tweetid = tweet.id
        text = tweet.text
        display(HTML(f"""<p><a href="https://twitter.com/{username}" target="_blank">{name}</a><br>
<a href="https://twitter.com/i/web/status/{tweetid}" target="_blank">{tweetid}</a><br>
{text}</p>"""))    



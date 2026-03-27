import requests

def expand_url(url, timeout=7):
    """
    Resolve shortened / redirecting URLs to their final destination.
    Uses GET (not HEAD) because many phishing sites block HEAD.
    """
    try:
        response = requests.get(
            url,
            allow_redirects=True,
            timeout=timeout,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            stream=True   # do NOT download body
        )
        return response.url
    except requests.RequestException:
        return url

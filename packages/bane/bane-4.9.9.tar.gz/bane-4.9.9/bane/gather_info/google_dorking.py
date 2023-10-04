from googlesearch import search

def google_dorking(
    q,
    max_results=100,
    language="en",
    start_from=1,
    stop_on=None,
    top_level_domain="com",
    pause=2,
):
    j = []
    j += search(
        q,
        num=max_results,
        lang=language,
        start=start_from,
        stop=stop_on,
        tld="com",
        pause=2,
    )
    l = []
    for x in j:
        if x not in l:
            l.append(x)
    return l


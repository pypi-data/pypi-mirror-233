from urllib.parse import urlparse


def _match_scheme(domain: str, pattern: str) -> bool:
    dom_scheme = urlparse(domain).scheme
    pat_scheme = urlparse(pattern).scheme
    return dom_scheme != "" and pat_scheme != "" and dom_scheme == pat_scheme


def _match_sub_domain(domain: str, pattern: str) -> bool:
    if not _match_scheme(domain, pattern):
        return False

    dom_netloc = urlparse(domain).netloc
    pat_netloc = urlparse(pattern).netloc

    if dom_netloc == "" or pat_netloc == "":
        return False

    if len(dom_netloc) > 253:  # domains over 253 characters aren't valid
        return False

    dom_comp = dom_netloc.split(".")
    pat_comp = pat_netloc.split(".")

    for i, v in enumerate(dom_comp):
        if len(pat_comp) <= i:
            return False
        p = pat_comp[i]
        if p == "*":
            return True
        if p != v:
            return False

    return False

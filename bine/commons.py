import urllib.request


class BookSearch:
    NAVER_OPEN_API = "http://openapi.naver.com/search"
    API_KEY = "c1b406b32dbbbbeee5f2a36ddc14067f"

    def search(self, keyword):
        url = NAVER_OPEN_API
        urllib.request.urlopen("http://example.com/foo/bar").read()
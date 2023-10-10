import http.server
import socketserver
import requests
from bs4 import BeautifulSoup

PORT = 8000
BASE_URL = 'https://news.ycombinator.com/'


class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    """
    Class for handler that gonna listening request in certain PORT locally.
    """
    def do_GET(self):
        """
        Function that requests to Hacker News for get pages.
        Imitating browser get requests.
        """
        url = BASE_URL + self.path[1:]
        response = requests.get(url)

        if response.status_code != 200:
            return (f"Failed request to page at {url}!",
                    response.status_code)

        soup = BeautifulSoup(response.text, 'lxml')
        for tag in soup.find_all(['link', 'img', 'script']):
            # print(tag)
            if 'href' in tag.attrs:  # modifying urls for css and media
                tag['href'] = BASE_URL + tag['href']
            if 'src' in tag.attrs:
                tag['src'] = BASE_URL + tag['src']
            # print(tag)
            # print()

        self.modify_text(soup)
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(str(soup).encode())

    @staticmethod
    def modify_text(soup: BeautifulSoup):
        """
        Function for change text in html with our pattern!
        Exp: original - images, modified - images™
        """
        for tags in soup.find_all(string=True):  # finding all tags with text
            if tags.parent.name not in ('script', 'style'):
                words = tags.split()
                for i in range(len(words)):
                    if len(words[i]) == 6 and words[i].isalpha():
                        # modifying needed text
                        words[i] = words[i] + '™'
                tags.replace_with(' '.join(words))


if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), ProxyHandler) as server:
        print(f"http://127.0.0.1:{PORT}/")
        server.serve_forever()
        # Starting server that listen our request in loop

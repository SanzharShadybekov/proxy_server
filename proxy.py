import http.server
import mimetypes
import socketserver
import requests
import os
import re
from bs4 import BeautifulSoup

PORT = 8000
BASE_URL = 'https://news.ycombinator.com/'
STATIC = 'static'
LOCAL_URL = 'http://127.0.0.1:8000/'
BASE_DIR = os.path.dirname(__file__)


class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    """
    Class for handler that gonna listening request in certain PORT locally.
    """
    def do_GET(self):
        """
        Function that requests to Hacker News for get pages.
        Imitating browser get requests.
        """
        if self.path.startswith('/static/'):  # processing requests to static
            path_to_file = os.path.join(BASE_DIR + self.path)
            # print()
            # print('-------')
            # print(path_to_file, '!!!!!!!!!')
            if os.path.exists(path_to_file):
                self.send_response(200)
                content_type, _ = mimetypes.guess_type(path_to_file)
                self.send_header('Content-Type', content_type)
                self.end_headers()
                with open(path_to_file, 'rb') as file:
                    self.wfile.write(file.read())
                return
            else:
                print('Error in static')
                self.send_error(404, 'Page Not Found!')

        url = BASE_URL + self.path[1:]
        response = requests.get(url)
        if response.status_code != 200:
            self.send_error(404, 'Page Not Found!')

        soup = BeautifulSoup(response.text, 'lxml')
        for tag in soup.find_all(['link', 'img', 'script']):
            if 'href' in tag.attrs:  # modifying urls for css and media
                if '?' in tag['href']:  # deleting trash in file names
                    index = tag['href'].index('?')
                    tag['href'] = tag['href'][:index]
                filename = self._get_static_files(BASE_URL + tag['href'])
                tag['href'] = LOCAL_URL + filename

            if 'src' in tag.attrs:
                if '?' in tag['src']:
                    index = tag['src'].index('?')
                    tag['src'] = tag['src'][:index]
                filename = self._get_static_files(BASE_URL + tag['src'])
                tag['src'] = LOCAL_URL + filename

        self._modify_text(soup)
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(str(soup).encode())

    @staticmethod
    def _modify_text(soup: BeautifulSoup):
        """
        Function for change text in html with our pattern!
        Exp: original - images, modified - images™
        """
        for tags in soup.find_all(string=True):  # finding all tags with text
            if tags.parent.name not in ('script', 'style'):
                tags.replace_with(ProxyHandler._modify_words(tags))
                # words = tags.split()
                # for i in range(len(words)):
                #     if len(words[i]) == 6 and words[i].isalpha():
                #         # modifying needed text
                #         words[i] = words[i] + '™'
                # tags.replace_with(' '.join(words))

    @staticmethod
    def _modify_words(words):
        """
        Function to modify six-letter words with symbol ™
        """
        modified_words = re.sub(r'\b\w{6}\b',
                                lambda match: match.group() + '™',
                                words)
        return modified_words

    @staticmethod
    def _get_static_files(url: str):
        """
        Function to save media, css and js files as static files locally
        if files exists, saving 2nd time skipping
        """
        filename = os.path.join(STATIC, os.path.basename(url))
        if not os.path.exists(filename):
            response = requests.get(url)

            if response.status_code == 200:
                os.makedirs(STATIC, exist_ok=True)
                content = response.content

                if os.path.basename(url) == 'news.css':
                    ProxyHandler._get_static_files(BASE_URL + 'triangle.svg')
                    content = re.sub(r'url\("([^"]+)"\)',
                                     ProxyHandler._replace_css_url,
                                     content.decode('utf-8'))
                    content = content.encode('utf-8')

                with open(filename, 'wb') as file:
                    file.write(content)
        return filename

    @staticmethod
    def _replace_css_url(match):
        return f'url("http://127.0.0.1:8000/static/{match.group(1)}")'


if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), ProxyHandler) as server:
        print(f"http://127.0.0.1:{PORT}/")
        # Starting server that listen our request in loop
        server.serve_forever()

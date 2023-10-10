import unittest
from proxy import ProxyHandler
from bs4 import BeautifulSoup
# import requests
# from unittest.mock import MagicMock


class TestProxyServer(unittest.TestCase):
    def test_text_modification(self):
        test_html = '<html><body><p>This is a test: \
        images commit john snow</p></body></html>'

        soup = BeautifulSoup(test_html, 'html.parser')

        ProxyHandler.modify_text(soup)
        self.assertEqual(
            str(soup),
            '<html><body><p>This is a test: images™ \
            commit™ john snow</p></body></html>'
        )

    # TODO test for server response
    # def test_server_response(self, mock_requests_get):
    #     self.handler = ProxyHandler(  )
    #     self.handler.send_headers = MagicMock()
    #     mock_requests_get.return_value.status_code = 200
    #     PORT = 8000
    #     response = requests.get(f"")
    #     self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

import requests
import urllib
import pandas as pd
from requests_html import HTMLSession
from requests_html import HTML

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction


class DemoExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []

        def get_source(url):
            """Return the source code for the provided URL.

            Args:
                url (string): URL of the page to scrape.

            Returns:
                response (object): HTTP response object from requests_html.
            """

            try:
                session = HTMLSession()
                response = session.get(url)
                return response

            except requests.exceptions.RequestException as e:
                print(e)


        def scrape_google(query):
            query = urllib.parse.quote_plus(query)
            response = get_source("https://www.google.co.uk/search?q=" + query)

            links = list(response.html.absolute_links)
            google_domains = ('https://www.google.',
                              'https://google.',
                              'https://webcache.googleusercontent.',
                              'http://webcache.googleusercontent.',
                              'https://policies.google.',
                              'https://support.google.',
                              'https://maps.google.')

            for url in links[:]:
                if url.startswith(google_domains):
                    links.remove(url)
                else:
                    items.append(ExtensionResultItem(icon='images/icon.png',
                                                     name=url,
                                                     description=url,
                                                     on_enter=HideWindowAction()))

            return links

        return RenderResultListAction(items)

if __name__ == '__main__':
    DemoExtension().run()
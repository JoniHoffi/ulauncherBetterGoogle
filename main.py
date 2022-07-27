from googlesearch import search

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction


class DemoExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []

        result = search(event.get_data(), num=1, stop=1, start=1, lang="de")

        for url in result:
            print(url)
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name=url,
                                             description=url,
                                             on_enter=OpenUrlAction(url)))

        print(items)
        return RenderResultListAction(items)

if __name__ == '__main__':
    DemoExtension().run()
from playwright.sync_api import Page

from error.element.exception import ElementException
from locations.location import Location


class DriverPage(object):
    _page = None

    def __init__(self, page: Page):
        self._page = page

    @property
    def page(self):
        return self._page

    def get_elements(self, location: Location):
        return self._page.query_selector_all(location.value)

    def get_element(self, location: Location):
        return self._page.query_selector(location.value)

    def click(self, location: Location):
        self._page.click(location.value)

    def refresh(self):
        self._page.reload()

    def get(self, url: str):
        self._page.goto(url)

    def screen(self, filename):
        self._page.screenshot(path=filename)

    def title(self):
        return self._page.title()

    def clear(self, location: Location):
        self._page.fill(location.value, "")

    def send(self, location: Location, text):
        self._page.fill(location.value, text)

    def click_text(self, location: Location, text: str, like=False):
        """
        @param location locations/定位对象
        @param text  matching text/匹配文本
        @param like: fuzzy match/模糊匹配
        """
        elements = self.get_elements(location.value)
        for e in elements:
            if like and text in e.text_content():
                e.click()
                return
            if not like and text == e.text_content():
                e.click()
                return
        else:
            raise ElementException(f"locations: [widget: {location.name} -> {location.value}] can't find {text}")

    def click_text_in_input(self, location: Location, text: str, like=False):
        """
        :param location locations/定位对象
        :param text  matching text/匹配文本
        :param like: fuzzy match/模糊匹配
        """
        elements = self.get_elements(location.value)
        for e in elements:
            if like and text in e.get_attribute("value"):
                e.click()
                return
            if not like and text == e.get_attribute("value"):
                e.click()
                return
        else:
            raise ElementException(f"locations: [widget: {location.name} -> {location.value}] can't find {text}")

    def attr(self, location: Location, attribute: str) -> str:
        """
        :param location
        :param attribute dom element's attribute such as "name"
        """
        return self.get_element(location.value).get_attribute(attribute)

    def text(self, location: Location):
        return self.get_element(location.value).text_content()

    def inner_text(self, location: Location):
        return self._page.inner_text(location.value)

    def inner_html(self, location: Location):
        return self._page.inner_html(location.value)

    def alert_accept(self):
        self._page.on('dialog', lambda dialog: dialog.accept())
        self._page.click('button')

    def alert_dismiss(self):
        self._page.on('dialog', lambda dialog: dialog.dismiss())
        self._page.click('button')

    def alert_msg(self):
        self._page.on('dialog', lambda dialog: print(dialog.message))

    def click_index(self, location: Location, index: int):
        if index < 0:
            raise ElementException("index is smaller than 0")
        elements = self.get_elements(location)
        if index > len(elements) - 1:
            raise ElementException(f"can't find element, index at {index} elements amount: {len(elements)}")
        elements[index].click()

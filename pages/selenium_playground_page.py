"""Page object for the Selenium Playground landing page (navigation links)."""

BASE_URL = "https://www.testmuai.com/selenium-playground/"


class SeleniumPlaygroundPage:
    def __init__(self, page):
        self.page = page

    def goto(self):
        self.page.goto(BASE_URL)

    def _open_link(self, link_name: str):
        self.page.get_by_role("link", name=link_name).click()
        # The destination pages are client-rendered (Next.js); wait for network
        # activity to settle so event handlers are hydrated before interacting.
        self.page.wait_for_load_state("networkidle")

    def open_simple_form_demo(self):
        # Locator strategy: role + accessible name
        self._open_link("Simple Form Demo")

    def open_drag_drop_sliders(self):
        self._open_link("Drag & Drop Sliders")

    def open_input_form_submit(self):
        self._open_link("Input Form Submit")

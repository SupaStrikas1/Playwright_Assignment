"""Page object for the 'Simple Form Demo' page (Single Input Field section)."""


class SimpleFormPage:
    def __init__(self, page):
        self.page = page
        # Locator strategy: accessible placeholder text
        self.message_input = page.get_by_placeholder("Please enter your Message")
        # Locator strategy: CSS id selector
        self.get_checked_value_button = page.locator("#showInput")
        self.displayed_message = page.locator("#message")

    def enter_message(self, text: str):
        self.message_input.fill(text)

    def click_get_checked_value(self):
        self.get_checked_value_button.click()

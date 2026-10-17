"""Page object for the 'Drag & Drop Sliders' page."""


class SliderPage:
    def __init__(self, page):
        self.page = page

    def _slider_container(self, label_text: str):
        # Locator strategy: XPath, located by the slider's visible label text
        return self.page.locator(
            f"xpath=//h4[contains(normalize-space(.), '{label_text}')]/parent::div"
        )

    def drag_slider_to(self, label_text: str, target_value: int):
        container = self._slider_container(label_text)
        range_input = container.locator("input[type='range']")
        range_input.click()
        range_input.focus()

        current_value = int(range_input.input_value())
        key = "ArrowRight" if target_value > current_value else "ArrowLeft"
        for _ in range(abs(target_value - current_value)):
            range_input.press(key)

    def get_range_value(self, label_text: str) -> str:
        container = self._slider_container(label_text)
        return container.locator("output").inner_text()

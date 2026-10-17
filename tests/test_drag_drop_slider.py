"""
Test Scenario 2:
1. Open the Selenium Playground and click "Drag & Drop Sliders".
2. Select the slider "Default value 15" and drag it to 95.
3. Validate the range value shows 95.
"""
from pages.selenium_playground_page import SeleniumPlaygroundPage
from pages.slider_page import SliderPage


def test_drag_slider_to_95(page):
    playground = SeleniumPlaygroundPage(page)
    playground.goto()
    playground.open_drag_drop_sliders()

    slider = SliderPage(page)
    slider.drag_slider_to("Default value 15", 95)

    assert slider.get_range_value("Default value 15") == "95"

"""
Test Scenario 1:
1. Open the Selenium Playground and click "Simple Form Demo".
2. Validate that the URL contains "simple-form-demo".
3. Enter a message into the "Enter Message" text box.
4. Click "Get Checked Value".
5. Validate that the same message is displayed under "Your Message:".
"""
from playwright.sync_api import expect

from pages.selenium_playground_page import SeleniumPlaygroundPage
from pages.simple_form_page import SimpleFormPage


def test_simple_form_demo_displays_entered_message(page):
    playground = SeleniumPlaygroundPage(page)
    playground.goto()
    playground.open_simple_form_demo()

    assert "simple-form-demo" in page.url

    simple_form = SimpleFormPage(page)
    message = "Welcome to TestMu AI"
    simple_form.enter_message(message)
    simple_form.click_get_checked_value()

    # Web-first assertion: auto-retries until the DOM reflects the click (Firefox
    # can commit the React state update a beat later than Chromium).
    expect(simple_form.displayed_message).to_have_text(message)

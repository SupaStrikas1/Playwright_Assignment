"""
Test Scenario 3:
1. Open the Selenium Playground and click "Input Form Submit".
2. Click "Submit" without filling in any information in the form.
3. Assert a "please fill in" validation error is raised.
4. Fill in Name, Email, and other fields; select Country "United States" by text.
5. Submit and validate the success message.

Note: this page relies on native HTML5 `required`-field validation rather than a
custom DOM error banner, so step 3 asserts the browser's constraint-validation
state/message (e.g. "Please fill out this field.") instead of a literal
"Please fill in the fields" string, which does not appear anywhere in the DOM.
"""
from pages.input_form_page import InputFormPage
from pages.selenium_playground_page import SeleniumPlaygroundPage


def test_input_form_submit_requires_fields_then_succeeds(page):
    playground = SeleniumPlaygroundPage(page)
    playground.goto()
    playground.open_input_form_submit()

    input_form = InputFormPage(page)

    # Step 2 & 3: submit empty form, expect native validation to block it.
    input_form.submit()
    assert input_form.is_form_valid() is False
    assert "fill" in input_form.get_name_field_validation_message().lower()

    # Step 4-6: fill in all required fields.
    input_form.fill_form(
        name="Jane Doe",
        email="jane.doe@example.com",
        password="SecurePass123!",
        company="Acme Corp",
        website="https://www.example.com",
        city="San Francisco",
        address1="123 Market Street",
        address2="Suite 500",
        state="California",
        zip_code="94104",
    )
    input_form.select_country("United States")
    input_form.submit()

    # Step 7: validate the success message.
    assert input_form.get_success_message() == (
        "Thanks for contacting us, we will get back to you shortly."
    )

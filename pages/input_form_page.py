"""Page object for the 'Input Form Submit' page (Input Form Validations section)."""


class InputFormPage:
    def __init__(self, page):
        self.page = page
        self.name_input = page.locator("#name")
        self.email_input = page.locator("#inputEmail4")
        self.password_input = page.locator("#inputPassword4")
        self.company_input = page.locator("#company")
        self.website_input = page.locator("#websitename")
        # Locator strategy: CSS attribute selector (no id on this element)
        self.country_select = page.locator("select[name='country']")
        self.city_input = page.locator("#inputCity")
        self.address1_input = page.locator("#inputAddress1")
        self.address2_input = page.locator("#inputAddress2")
        self.state_input = page.locator("#inputState")
        self.zip_input = page.locator("#inputZip")
        self.submit_button = page.locator("#seleniumform button[type='submit']")
        self.success_message = page.locator(".success-msg")

    def submit(self):
        self.submit_button.click()

    def get_name_field_validation_message(self) -> str:
        """The site relies on native HTML5 required-field validation (no custom
        error banner), so we read the browser's constraint-validation message
        for the first required field instead of a static DOM error message."""
        return self.name_input.evaluate("el => el.validationMessage")

    def is_form_valid(self) -> bool:
        return self.page.evaluate("document.querySelector('#seleniumform').checkValidity()")

    def select_country(self, country_text: str):
        self.country_select.select_option(label=country_text)

    def fill_form(
        self,
        name: str,
        email: str,
        password: str,
        company: str,
        website: str,
        city: str,
        address1: str,
        address2: str,
        state: str,
        zip_code: str,
    ):
        self.name_input.fill(name)
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.company_input.fill(company)
        self.website_input.fill(website)
        self.city_input.fill(city)
        self.address1_input.fill(address1)
        self.address2_input.fill(address2)
        self.state_input.fill(state)
        self.zip_input.fill(zip_code)

    def get_success_message(self) -> str:
        return self.success_message.inner_text()

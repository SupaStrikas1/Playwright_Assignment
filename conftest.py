"""Shared pytest fixtures: connects Playwright to the TestMu AI (LambdaTest) cloud grid.

Running `pytest -n <N>` (pytest-xdist) distributes the parametrized `capability`
fixture values across worker processes, so the browser/OS combinations below are
executed in parallel on TestMu AI.
"""
import json
import urllib.parse
from datetime import datetime

import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from utils.lambdatest_capabilities import build_capabilities

load_dotenv()

LT_CDP_URL = "wss://cdp.lambdatest.com/playwright"
BUILD_NAME = f"Playwright 101 - Selenium Playground ({datetime.now().strftime('%Y-%m-%d %H:%M')})"

# At least 2 different browser/OS combinations, executed in parallel via pytest-xdist.
# Both combinations use real, CDP-based browsers (not Playwright's bundled pw-firefox
# build) because Firefox's "Juggler" remote protocol is version-sensitive between the
# local Playwright client and LambdaTest's grid-side bundled Firefox build, which caused
# TargetClosedError failures on every pw-firefox session regardless of the connect fix.
CAPABILITY_MATRIX = [
    {"id": "chrome-win10", "browser_name": "Chrome", "platform": "Windows 10"},
    {"id": "edge-win10", "browser_name": "MicrosoftEdge", "platform": "Windows 10"},
]

# LambdaTest's Playwright CDP endpoint speaks a different wire protocol per remote
# browser engine, so the client must connect using the matching Playwright browser
# type (chromium.connect() for Chrome/Edge, firefox.connect() for pw-firefox, etc.)
# or the pipe is torn down immediately with a TargetClosedError.
BROWSER_TYPE_FOR_CAPABILITY = {
    "Chrome": "chromium",
    "MicrosoftEdge": "chromium",
    "pw-chromium": "chromium",
    "pw-firefox": "firefox",
    "pw-webkit": "webkit",
}


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Stash the test outcome on the item so the `page` fixture can report pass/fail to LambdaTest."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def pytest_addoption(parser):
    parser.addoption(
        "--local",
        action="store_true",
        default=False,
        help="Run tests against local Playwright browsers instead of the LambdaTest cloud grid.",
    )


@pytest.fixture(params=CAPABILITY_MATRIX, ids=[c["id"] for c in CAPABILITY_MATRIX])
def capability(request):
    return request.param


@pytest.fixture
def page(request, capability):
    browser_type_name = BROWSER_TYPE_FOR_CAPABILITY.get(capability["browser_name"], "chromium")

    with sync_playwright() as playwright:
        browser_type = getattr(playwright, browser_type_name)

        if request.config.getoption("--local"):
            # Local dry-run: launch a real local browser, skip the LambdaTest grid entirely.
            browser = browser_type.launch(headless=True)
            context = browser.new_context()
            local_page = context.new_page()

            yield local_page

            context.close()
            browser.close()
            return

        test_name = f"{request.node.name} [{capability['id']}]"
        capabilities = build_capabilities(
            browser_name=capability["browser_name"],
            platform=capability["platform"],
            test_name=test_name,
            build_name=BUILD_NAME,
        )
        ws_endpoint = f"{LT_CDP_URL}?capabilities={urllib.parse.quote(json.dumps(capabilities))}"
        browser = browser_type.connect(ws_endpoint)
        context = browser.new_context()
        lt_page = context.new_page()

        yield lt_page

        report = getattr(request.node, "rep_call", None)
        status = "passed" if report is not None and report.passed else "failed"
        remark = "Test completed successfully" if status == "passed" else "Test assertion failed"
        status_payload = json.dumps({"action": "setTestStatus", "arguments": {"status": status, "remark": remark}})
        try:
            lt_page.evaluate("_ => {}", f"lambdatest_action: {status_payload}")
        except Exception:
            pass

        context.close()
        browser.close()

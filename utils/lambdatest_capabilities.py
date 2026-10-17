"""Builds LambdaTest (TestMu AI) capability payloads for Playwright CDP sessions."""
import os


def build_capabilities(browser_name: str, platform: str, test_name: str, build_name: str) -> dict:
    """Return the capabilities dict required by LambdaTest's Playwright CDP endpoint.

    browser_name: one of "Chrome", "MicrosoftEdge", "pw-chromium", "pw-firefox", "pw-webkit".
    platform: OS name as recognized by LambdaTest, e.g. "Windows 10".
    """
    return {
        "browserName": browser_name,
        "browserVersion": "latest",
        "LT:Options": {
            "platform": platform,
            "build": build_name,
            "name": test_name,
            "user": os.environ["LT_USERNAME"],
            "accessKey": os.environ["LT_ACCESS_KEY"],
            "network": True,
            "video": True,
            "console": True,
            "visual": True,
        },
    }

import pytest
import allure
from playwright.sync_api import Page, expect, Browser, BrowserContext
import os
from pathlib import Path

BASE_URL = os.getenv("BASE_URL", "http://localhost:5137")
API_URL = os.getenv("API_URL", "http://localhost:8888")

@pytest.fixture(scope="session")
def browser():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def context(browser: Browser):
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="ru-RU"
    )
    # Start tracing
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield context
    # Stop tracing and save if test failed
    if hasattr(context, '_test_failed') and context._test_failed:
        trace_path = f"traces/test_trace_{context._test_name}.zip"
        context.tracing.stop(path=trace_path)
        allure.attach.file(trace_path, name="Playwright Trace", attachment_type='application/zip')
    else:
        context.tracing.stop()
    context.close()

@pytest.fixture(scope="function")
def page(context: BrowserContext, request):
    page = context.new_page()
    page.set_default_timeout(15000)
    
    # Set test name for trace naming
    context._test_name = request.node.name
    context._test_failed = False
    
    yield page
    
    # Screenshot on failure
    if request.node.rep_call.failed:
        context._test_failed = True
        screenshot = page.screenshot(full_page=True)
        allure.attach(screenshot, name="Screenshot", attachment_type=allure.attachment_type.PNG)
    
    page.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

@pytest.fixture(scope="function", autouse=True)
def allure_setup(request):
    """Автоматически добавляет Allure-аннотации из имени теста."""
    test_name = request.node.name.replace("test_", "").replace("_", " ").title()
    allure.dynamic.title(test_name)
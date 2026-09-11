import pytest
import allure
import requests
from playwright.sync_api import Page, expect, Browser, BrowserContext
import os
from pathlib import Path

BASE_URL = os.getenv("BASE_URL", "http://localhost:5137")
API_URL = os.getenv("API_URL", "http://localhost:8888")

EMAIL = 'test@example.com'
PASSWORD = 'password123'

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

    rep_call = getattr(request.node, "rep_call", None)
    rep_setup = getattr(request.node, "rep_setup", None)
    failed = (rep_call is not None and rep_call.failed) or (rep_setup is not None and rep_setup.failed)
    if failed:
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

@pytest.fixture(scope="session", autouse=True)
def ensure_seed_user():
    """Гарантирует наличие фиксированного тестового аккаунта, не полагаясь
    на то, что кто-то когда-то создал его вручную или в прошлом прогоне.
    Работает независимо от того, чистится БД между прогонами или нет."""
    try:
        requests.post(
            f"{API_URL}/api/auth/register",
            json={
                "email": EMAIL,
                "first_name": "Test",
                "last_name": "User",
                "phone": "",
                "password": PASSWORD,
            },
            timeout=10,
        )
    except requests.RequestException:
        pass
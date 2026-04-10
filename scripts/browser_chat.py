#!/usr/bin/env python3
"""
Browser-based AI Chat via Playwright
Supports Gemini and ChatGPT web interfaces (free versions)

Usage:
    from browser_chat import chat_via_browser
    result = chat_via_browser(model="gemini", prompt="Hello!")
    print(result)
"""

import os
import json
import time
import sys
import signal
from pathlib import Path

BROWSER_TIMEOUT = 90  # seconds - force kill if browser hangs


class BrowserTimeoutError(Exception):
    pass


def _timeout_handler(signum, frame):
    raise BrowserTimeoutError(f"Browser operation timed out after {BROWSER_TIMEOUT}s")


def _with_timeout(func, *args, **kwargs):
    """Run func with SIGALRM timeout. Restores alarm on any exit."""
    old_handler = signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(BROWSER_TIMEOUT)
    try:
        return func(*args, **kwargs)
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)


try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("ERROR: Playwright not installed. Run: pip3 install playwright --break-system-packages && python3 -m playwright install chromium")
    sys.exit(1)

# Default Chromium path for Playwright
DEFAULT_CHROMIUM_PATH = "/root/.cache/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-linux64/chrome-headless-shell"

def get_browser_context(pw, proxy: str = None):
    """Launch browser with appropriate settings. Caller MUST call browser.close() in a finally block."""
    launch_args = [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
        "--disable-blink-features=AutomationControlled",
        "--disable-web-security",
    ]
    proxy_config = None
    if proxy:
        proxy_config = {"server": proxy}
        print(f"[Browser] Using proxy: {proxy}", file=sys.stderr)
    
    browser = pw.chromium.launch(
        headless=True,
        executable_path=os.environ.get("BROWSER_CHROMIUM_PATH", DEFAULT_CHROMIUM_PATH),
        args=launch_args,
        proxy=proxy_config,
    )
    context = browser.contexts[0] if browser.contexts else browser.new_context(
        viewport={"width": 1280, "height": 800},
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    return browser, context


def chat_gemini_web(prompt: str, cookies_path: str = None, proxy: str = None) -> dict:
    """
    Chat via Gemini web (gemini.google.com).
    
    Args:
        prompt: The message to send to Gemini
        cookies_path: Optional path to load/save session cookies
        proxy: Optional proxy URL (e.g., "http://clash:7890")
        
    Returns:
        {"success": bool, "response": str, "error": str or None}
    """
    browser = None
    try:
        def _do_chat():
            nonlocal browser
            with sync_playwright() as pw:
                browser, context = get_browser_context(pw, proxy=proxy)
                page = context.new_page()
                
                page.set_extra_http_headers({
                    "Accept-Language": "en-US,en;q=0.9",
                })
                
                if cookies_path and os.path.exists(cookies_path):
                    with open(cookies_path) as f:
                        context.add_cookies(json.load(f))
                
                page.goto("https://gemini.google.com", timeout=60000)
                try:
                    page.wait_for_load_state("networkidle", timeout=30000)
                except:
                    pass
                time.sleep(3)
                
                input_box = page.query_selector("[contenteditable='true'][role='textbox']")
                
                if not input_box:
                    body_text = page.inner_text("body")
                    if "Sign in" in body_text and "Meet Gemini" not in body_text:
                        result["error"] = "Login required. Please provide cookies or log in manually."
                    else:
                        result["error"] = "Could not find Gemini input box (contenteditable textbox)"
                    return
                
                input_box.click()
                time.sleep(0.5)
                input_box.fill(prompt)
                time.sleep(1)
                input_box.press("Enter")
                time.sleep(2)
                
                response_appeared = False
                for wait_round in range(12):
                    time.sleep(5)
                    try:
                        page.wait_for_load_state("networkidle", timeout=10000)
                    except:
                        pass
                    
                    current_body = page.inner_text("body")
                    
                    if "Something went wrong" in current_body:
                        if wait_round < 3:
                            page.reload(timeout=30000)
                            time.sleep(3)
                            input_box = page.query_selector("[contenteditable='true'][role='textbox']")
                            if input_box:
                                input_box.click()
                                time.sleep(0.5)
                                input_box.fill(prompt)
                                time.sleep(1)
                                input_box.press("Enter")
                            continue
                        else:
                            result["error"] = "Gemini returned 'Something went wrong' error"
                            return
                    
                    lines = current_body.split("\n")
                    prompt_lines = [l for l in lines if prompt[:30] in l]
                    if prompt_lines:
                        prompt_idx = lines.index(prompt_lines[0])
                        after_prompt = "\n".join(lines[prompt_idx+1:])
                        noise = ["Sign in", "Gemini", "About Gemini", "Tools", "Fast",
                                 "Google Terms", "Google Privacy Policy", "Submit",
                                 "Subscriptions", "For Business", "Opens in a new window",
                                 "Write", "Plan", "Research", "Learn", "Meet Gemini",
                                 "Conversation with Gemini", "message", "aria-label"]
                        response_lines = [l.strip() for l in after_prompt.split("\n")
                                        if l.strip() and not any(n.lower() in l.lower() for n in noise)]
                        if response_lines:
                            result["success"] = True
                            result["response"] = "\n".join(response_lines[:20])
                            response_appeared = True
                            break
                
                if not response_appeared and not result["error"]:
                    result["error"] = "No response received from Gemini (timeout)"
                
                if cookies_path and result["success"]:
                    with open(cookies_path, "w") as f:
                        json.dump(context.cookies(), f)
        
        _with_timeout(_do_chat)
        
    except BrowserTimeoutError as e:
        result["error"] = str(e)
    except Exception as e:
        result["error"] = str(e)
    finally:
        if browser:
            try:
                browser.close()
            except Exception:
                pass
    
    return result


def chat_chatgpt_web(prompt: str, cookies_path: str = None, proxy: str = None) -> dict:
    """
    Chat via ChatGPT web (chatgpt.com).
    
    Args:
        prompt: The message to send to ChatGPT
        cookies_path: Optional path to load/save session cookies
        proxy: Optional proxy URL (e.g., "http://clash:7890")
        
    Returns:
        {"success": bool, "response": str, "error": str or None}
    """
    browser = None
    try:
        def _do_chat():
            nonlocal browser
            with sync_playwright() as pw:
                browser, context = get_browser_context(pw, proxy=proxy)
                page = context.new_page()
                
                if cookies_path and os.path.exists(cookies_path):
                    with open(cookies_path) as f:
                        context.add_cookies(json.load(f))
                
                page.goto("https://chatgpt.com", timeout=30000)
                page.wait_for_load_state("networkidle", timeout=15000)
                time.sleep(2)
                
                try:
                    input_area = page.query_selector("textarea")
                    if not input_area:
                        login_btn = page.query_selector("text=Log in")
                        if login_btn:
                            result["error"] = "Login required. Please provide cookies or log in manually."
                            return
                except:
                    pass
                
                input_box = None
                for selector in [
                    "textarea[placeholder*='Message'], textarea[placeholder*='ChatGPT']",
                    "div[contenteditable='true'][data-tab-focus='true']",
                    "textarea",
                ]:
                    try:
                        el = page.query_selector(selector)
                        if el and el.is_visible():
                            input_box = el
                            break
                    except:
                        continue
                
                if not input_box:
                    result["error"] = "Could not find ChatGPT input box"
                    return
                
                input_box.click()
                time.sleep(0.5)
                input_box.fill(prompt)
                time.sleep(0.5)
                
                send_btn = None
                for selector in [
                    "button[aria-label*='Send']",
                    "button:has-text('Send')",
                    "button:has-text('Submit')",
                ]:
                    try:
                        btn = page.query_selector(selector)
                        if btn and btn.is_visible():
                            send_btn = btn
                            break
                    except:
                        continue
                
                if send_btn:
                    send_btn.click()
                else:
                    input_box.press("Enter")
                
                page.wait_for_load_state("networkidle", timeout=30000)
                time.sleep(4)
                
                response_text = ""
                for selector in [
                    "[data-message-author-role='assistant']",
                    ".markdown-result",
                    "div[class*='response']",
                    "[class*='Message']",
                ]:
                    try:
                        elements = page.query_selector_all(selector)
                        if elements:
                            response_text = elements[-1].inner_text()
                            if response_text.strip():
                                break
                    except:
                        continue
                
                if not response_text or not response_text.strip():
                    try:
                        main_area = page.query_selector("main") or page
                        response_text = main_area.inner_text()[-3000:]
                    except:
                        response_text = page.inner_text("body")[-3000:]
                
                result["success"] = True
                result["response"] = response_text.strip()
                
                if cookies_path:
                    with open(cookies_path, "w") as f:
                        json.dump(context.cookies(), f)
        
        _with_timeout(_do_chat)
        
    except BrowserTimeoutError as e:
        result["error"] = str(e)
    except Exception as e:
        result["error"] = str(e)
    finally:
        if browser:
            try:
                browser.close()
            except Exception:
                pass
    
    return result


def chat_via_browser(model: str, prompt: str, cookies_path: str = None, proxy: str = None) -> str:
    """
    Universal interface for browser-based AI chat.
    
    Args:
        model: "gemini" or "chatgpt"
        prompt: The message to send
        cookies_path: Optional path to load/save session cookies for persistent login
        proxy: Optional proxy URL (e.g., "http://clash:7890")
        
    Returns:
        The AI's response text, or error message
    """
    model = model.lower().strip()
    
    if model in ("gemini", "gemini-web"):
        result = chat_gemini_web(prompt, cookies_path, proxy=proxy)
    elif model in ("chatgpt", "gpt", "openai"):
        result = chat_chatgpt_web(prompt, cookies_path, proxy=proxy)
    else:
        return f"ERROR: Unknown model '{model}'. Use 'gemini' or 'chatgpt'."
    
    if result["success"]:
        return result["response"]
    else:
        return f"ERROR: {result['error']}"


if __name__ == "__main__":
    # CLI test
    import argparse
    parser = argparse.ArgumentParser(description="Browser-based AI Chat")
    parser.add_argument("--model", "-m", default="gemini", choices=["gemini", "chatgpt"])
    parser.add_argument("--prompt", "-p", required=True)
    parser.add_argument("--cookies", "-c", default=None, help="Path to cookies file for persistent login")
    parser.add_argument("--proxy", default=None, help="Proxy URL (e.g., http://clash:7890)")
    args = parser.parse_args()
    
    response = chat_via_browser(args.model, args.prompt, args.cookies, proxy=args.proxy)
    print(response)

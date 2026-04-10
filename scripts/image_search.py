#!/usr/bin/env python3
"""
图片搜索引擎 - 在 bge-embedding 容器中通过 Playwright 搜索高质量配图

功能：
- 在 Unsplash / Pexels / NIH NLM / Science Photo Library 等平台搜索科学配图
- 返回可商用的图片 URL 列表

用法：
    python3 image_search.py --query "human brain MRI GLP-1" --site unsplash --max 5
    python3 image_search.py --query "neuroinflammation microglia" --site nih --max 5
"""

import argparse
import json
import sys
import time
import urllib.parse

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("ERROR: Playwright not installed in this environment", file=sys.stderr)
    sys.exit(1)

# Chromium path
DEFAULT_CHROMIUM = "/root/.cache/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-linux64/chrome-headless-shell"

SEARCH_CONFIGS = {
    "unsplash": {
        "url": "https://unsplash.com/s/photos/{query}",
        "selector": "a[aria-label*='Photo' i]",
        "attr": "href",
        "page_load_wait": 3,
        "scroll": 2,
        "example_url": "https://unsplash.com/photos/{id}",
    },
    "pexels": {
        "url": "https://www.pexels.com/search/{query}/",
        "selector": "a[href*='/photo/']",
        "attr": "href",
        "page_load_wait": 3,
        "scroll": 2,
        "example_url": "https://www.pexels.com/photo/{id}",
    },
    "nih": {
        "url": "https://images.nlm.nih.gov/?{query}",
        "selector": "a.SearchResultItem",
        "attr": "href",
        "page_load_wait": 4,
        "scroll": 2,
        "example_url": "https://images.nlm.nih.gov/{id}",
    },
    "sciencephoto": {
        "url": "https://www.sciencephoto.com/search?text={query}",
        "selector": "a.thumb-link",
        "attr": "href",
        "page_load_wait": 3,
        "scroll": 2,
        "example_url": "https://www.sciencephoto.com/{id}",
    },
    "bing_images": {
        "url": "https://cn.bing.com/images/search?q={query}&ensearch=1",
        "selector": "a.iusc",
        "attr": "href",
        "page_load_wait": 3,
        "scroll": 2,
        "example_url": "",
    },
}

PROXY = "http://172.17.0.2:7890"  # mihomo on host


def check_mihomo():
    """检查 mihomo 是否可用（5秒超时），不可用返回 False"""
    import subprocess
    try:
        r = subprocess.run(
            ["curl", "-sf", "--connect-timeout", "5", "-m", "5", "http://clash:9090/proxies"],
            capture_output=True, timeout=8
        )
        return r.returncode == 0
    except: return False


def search_images(query: str, site: str = "bing_images", max_results: int = 5) -> dict:
    """搜索图片，返回 URL 列表"""
    
    # mihomo 挂了直接返回空结果，不卡死
    if not check_mihomo():
        return {"query": query, "site": site, "results": [], "error": "mihomo unavailable"}
    
    config = SEARCH_CONFIGS.get(site, SEARCH_CONFIGS["bing_images"])
    encoded_query = urllib.parse.quote(query)
    url = config["url"].format(query=encoded_query)
    
    results = {
        "query": query,
        "site": site,
        "results": [],
        "error": None,
    }
    
    chromium_path = DEFAULT_CHROMIUM
    
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(
                headless=True,
                executable_path=chromium_path,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-blink-features=AutomationControlled",
                ],
                proxy={"server": PROXY} if PROXY else None,
            )
            
            context = browser.new_context(
                viewport={"width": 1280, "height": 900},
                user_agent=(
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                ),
            )
            page = context.new_page()
            
            print(f"[ImageSearch] Navigating to {url}", file=sys.stderr)
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(config["page_load_wait"] * 1000)
            
            # Scroll to load more images
            for _ in range(config["scroll"]):
                page.evaluate("window.scrollBy(0, 600)")
                page.wait_for_timeout(1500)
            
            # Extract image links + nested img srcs
            links = []
            img_srcs = []
            try:
                elements = page.query_selector_all(config["selector"])
                for el in elements[:max_results + 10]:
                    href = el.get_attribute(config["attr"])
                    img = el.query_selector("img")
                    img_src = img.get_attribute("src") if img else None
                    if href:
                        full_url = href if href.startswith("http") else f"https://cn.bing.com{href}"
                        if full_url not in links:
                            links.append(full_url)
                    if img_src and img_src.startswith("http") and img_src not in img_srcs:
                        img_srcs.append(img_src)
            except Exception as e:
                results["error"] = f"Selector error: {e}"
            
            # For Bing: visit detail page to get original (full-size) source URL
            if site == "bing_images" and links:
                original_urls = []
                for detail_url in links[:max_results]:
                    resolved = _resolve_bing_thumbnail_to_original(PROXY, chromium_path, detail_url, timeout=15)
                    if resolved:
                        original_urls.append(resolved)
                    else:
                        # Fallback: use thumbnail URL
                        img_id = detail_url.split("id=")[1].split("&")[0] if "id=" in detail_url else ""
                        img_match = [s for s in img_srcs if img_id in s] if img_id else []
                        original_urls.append(img_match[0] if img_match else detail_url)
                results["results"] = original_urls
                results["has_original_urls"] = any(u for u in original_urls if "/th/" not in u)
            else:
                results["results"] = links[:max_results]
            
            browser.close()
            
    except Exception as e:
        results["error"] = str(e)
    
    return results


def _resolve_bing_thumbnail_to_original(proxy, chromium_path, detail_url, timeout=15):
    """从 Bing 详情 URL 提取 mediaurl 参数（无需访问页面）"""
    try:
        from urllib.parse import unquote, parse_qs, urlparse
        parsed = urlparse(detail_url)
        qs = parse_qs(parsed.query)
        mediaurl = qs.get("mediaurl", [None])[0]
        if mediaurl:
            return unquote(mediaurl)
        return None
    except Exception:
        return None


def main():
    parser = argparse.ArgumentParser(description="图片搜索引擎")
    parser.add_argument("--query", "-q", required=True, help="搜索关键词")
    parser.add_argument("--site", "-s", default="bing_images",
                        choices=list(SEARCH_CONFIGS.keys()),
                        help="搜索平台")
    parser.add_argument("--max", "-m", type=int, default=5, help="最大结果数")
    parser.add_argument("--output", "-o", help="输出文件路径（JSON）")
    
    args = parser.parse_args()
    
    result = search_images(args.query, args.site, args.max)
    
    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[ImageSearch] Results saved to {args.output}", file=sys.stderr)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # Exit code
    sys.exit(0 if not result["error"] else 1)


if __name__ == "__main__":
    main()

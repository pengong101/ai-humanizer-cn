#!/usr/bin/env python3
"""Multi-engine search via mihomo proxy - returns unified JSON"""
import subprocess, json, re, sys, urllib.parse, time

MIHOMO_PROXY = "http://clash:7890"

def check_mihomo():
    """检查 mihomo 是否可用（5秒超时），不可用返回 False"""
    try:
        r = subprocess.run(
            ["curl", "-sf", "--connect-timeout", "5", "-m", "5", "http://clash:9090/proxies"],
            capture_output=True, timeout=8
        )
        return r.returncode == 0
    except: return False

ENGINES = {
    "bing": {
        "url": "https://cn.bing.com/search?q={q}&format=rss",
        "parser": "rss",
        "timeout": 12,
    },
    "searxng_bing": {
        "url": "http://searxng:8080/search?q={q}&format=json&engines=bing",
        "parser": "json",
        "timeout": 15,
    },
    "searxng_baidu": {
        "url": "http://searxng:8080/search?q={q}&format=json&engines=baidu",
        "parser": "json",
        "timeout": 15,
    },
}

def curl(url, proxy=MIHOMO_PROXY, timeout=12, headers=None):
    h = headers or ["User-Agent: Mozilla/5.0 (compatible)", "Accept: */*"]
    cmd = ["curl", "--max-time", str(timeout), "-x", proxy, "-H", h[0], "-H", h[1] if len(h) > 1 else "", url]
    cmd = [c for c in cmd if c]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout+5)
    return r.stdout if r.returncode == 0 else ""

def parse_rss(xml):
    items = []
    for im in re.finditer(r"<item>([\s\S]*?)</item>", xml):
        ix = im.group(1)
        def g(t): m = re.search(f"<{t}[^>]*>([^<]*)</{t}>", ix); return m.group(1).strip() if m else ""
        link = g("link")
        if link:
            items.append({"title": re.sub(r"<[^>]+>", "", g("title"))[:200], 
                        "url": link, "description": re.sub(r"<[^>]+>", "", g("description"))[:300],
                        "pubDate": g("pubDate"), "source": "bing_rss"})
    return items

def parse_searxng_json(text):
    try:
        d = json.loads(text)
        return [{"title": r.get("title","")[:200], "url": r.get("url",""), 
                 "description": r.get("content", r.get("snippet",""))[:300],
                 "pubDate": "", "source": r.get("engine","")} 
                for r in d.get("results",[])[:15] if r.get("url")]
    except: return []

def search(query, engines=None, max_results=20):
    # mihomo 挂了直接返回空结果，不卡死
    if not check_mihomo():
        return {"query": query, "total": 0, "results": [], "error": "mihomo unavailable"}
    
    engines = engines or ["bing", "searxng_bing", "searxng_baidu"]
    all_results, seen_urls = [], set()
    
    for name in engines:
        cfg = ENGINES.get(name)
        if not cfg: continue
        url = cfg["url"].replace("{q}", urllib.parse.quote(query))
        xml = curl(url, timeout=cfg["timeout"])
        if not xml: continue
        
        items = parse_rss(xml) if cfg["parser"] == "rss" else parse_searxng_json(xml)
        
        for item in items:
            url_key = item["url"].split("?")[0].lower()
            if url_key and url_key not in seen_urls:
                seen_urls.add(url_key)
                all_results.append(item)
        
        if len(all_results) >= max_results:
            break
    
    return {"query": query, "total": len(all_results), "results": all_results[:max_results]}

if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "AI"
    result = search(q, max_results=20)
    print(json.dumps(result, indent=2, ensure_ascii=False))

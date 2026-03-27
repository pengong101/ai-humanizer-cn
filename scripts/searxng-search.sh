#!/bin/bash
# SearXNG 搜索脚本 - 直连容器内 IP
QUERY=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$1'))")
ENGINE="${2:-google}"
FORMAT="${3:-json}"
curl -s "http://172.18.0.3:8080/search?q=${QUERY}&engines=${ENGINE}&format=${FORMAT}" --max-time 15

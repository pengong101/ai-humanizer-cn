#!/bin/bash
# Daily Archive Script
# Author: pengong101
# Runs at 23:00 daily

DATE=$(date +%Y%m%d)
ARCHIVE_DIR="/root/.openclaw/workspace/archive/$(date +%Y)/$(date +%m)/$(date +%d)"

echo "📅 Daily Archive - $DATE"
echo "================================"

# Create archive directory
mkdir -p "$ARCHIVE_DIR"

# Copy daily artifacts
cp /root/.openclaw/workspace/*.tar.gz "$ARCHIVE_DIR/" 2>/dev/null
cp /root/.openclaw/workspace/*.md "$ARCHIVE_DIR/" 2>/dev/null
cp /root/.openclaw/workspace/CLAWHUB-DEPLOY/*.yaml "$ARCHIVE_DIR/" 2>/dev/null

# Create index
cat > "$ARCHIVE_DIR/INDEX.md" << INDEXEOF
# Daily Archive Index - $(date +%Y-%m-%d)

## Files 文件
$(ls -1 "$ARCHIVE_DIR" 2>/dev/null)

## Summary 总结
- Skills packaged: $(ls "$ARCHIVE_DIR"/*.tar.gz 2>/dev/null | wc -l)
- Documents: $(ls "$ARCHIVE_DIR"/*.md 2>/dev/null | wc -l)
- Deploy files: $(ls "$ARCHIVE_DIR"/*.yaml 2>/dev/null | wc -l)

## Author
pengong101
INDEXEOF

echo "✅ Daily archive completed: $ARCHIVE_DIR"

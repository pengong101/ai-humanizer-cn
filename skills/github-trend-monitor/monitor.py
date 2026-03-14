#!/usr/bin/env python3
"""
GitHub Trend Monitor - GitHub 热点监控工具
版本：v1.0.0
功能：实时监控 GitHub Trending，中文摘要生成，热点推送
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path


class GitHubTrendMonitor:
    """GitHub 热点监控器"""
    
    def __init__(self, config_path: str = None):
        """
        初始化监控器
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path or os.path.expanduser('~/.openclaw/trend-monitor.json')
        self.data_dir = os.path.expanduser('~/.openclaw/trend-data')
        self.trends_file = os.path.join(self.data_dir, 'trends.json')
        
        # 确保目录存在
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 加载配置
        self.config = self._load_config()
        
        # GitHub Trending URL
        self.trending_url = 'https://github.com/trending'
        self.developers_url = 'https://github.com/trending/developers'
    
    def _load_config(self) -> Dict:
        """加载配置文件"""
        default_config = {
            'keywords': ['AI', 'OpenClaw', 'agent', 'automation', 'LLM'],
            'languages': ['Python', 'JavaScript', 'TypeScript'],
            'since': 'daily',  # daily, weekly, monthly
            'notify': True,
            'summary_language': 'zh-CN'
        }
        
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return {**default_config, **config}
        
        return default_config
    
    def _save_config(self):
        """保存配置文件"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def fetch_trending(self, since: str = 'daily') -> List[Dict]:
        """
        获取 GitHub Trending
        
        Args:
            since: 时间范围 (daily/weekly/monthly)
        
        Returns:
            List[Dict]: Trending 项目列表
        """
        print(f"📊 获取 GitHub Trending ({since})...")
        
        # 简化实现 - 实际应调用 GitHub API 或爬取网页
        # 这里返回模拟数据用于演示
        mock_trends = [
            {
                'name': 'openclaw/skills',
                'description': 'OpenClaw Skills Collection - 1700+ AI Agent Skills',
                'language': 'Python',
                'stars': 1234,
                'forks': 234,
                'url': 'https://github.com/openclaw/skills'
            },
            {
                'name': 'pengong101/ai-humanizer-cn',
                'description': 'AI 文本优化工具 - 让 AI 写作更像真人',
                'language': 'Python',
                'stars': 567,
                'forks': 89,
                'url': 'https://github.com/pengong101/ai-humanizer-cn'
            },
            {
                'name': 'openclaw/openclaw',
                'description': 'OpenClaw - Open Source AI Agent Framework',
                'language': 'TypeScript',
                'stars': 2345,
                'forks': 456,
                'url': 'https://github.com/openclaw/openclaw'
            }
        ]
        
        print(f"✅ 获取到 {len(mock_trends)} 个 trending 项目")
        return mock_trends
    
    def filter_by_keywords(self, trends: List[Dict]) -> List[Dict]:
        """
        根据关键词过滤
        
        Args:
            trends: Trending 项目列表
        
        Returns:
            List[Dict]: 过滤后的项目
        """
        filtered = []
        keywords = self.config.get('keywords', [])
        
        for trend in trends:
            name = trend.get('name', '').lower()
            desc = trend.get('description', '').lower()
            
            # 检查是否包含关键词
            for keyword in keywords:
                if keyword.lower() in name or keyword.lower() in desc:
                    filtered.append(trend)
                    break
        
        print(f"🔍 关键词过滤：{len(filtered)}/{len(trends)}")
        return filtered
    
    def filter_by_language(self, trends: List[Dict]) -> List[Dict]:
        """
        根据编程语言过滤
        
        Args:
            trends: Trending 项目列表
        
        Returns:
            List[Dict]: 过滤后的项目
        """
        languages = self.config.get('languages', [])
        if not languages:
            return trends
        
        filtered = [t for t in trends if t.get('language') in languages]
        print(f"💻 语言过滤：{len(filtered)}/{len(trends)}")
        return filtered
    
    def generate_summary(self, trends: List[Dict]) -> str:
        """
        生成中文摘要
        
        Args:
            trends: Trending 项目列表
        
        Returns:
            str: 中文摘要
        """
        summary = []
        summary.append("# GitHub Trending 日报")
        summary.append(f"**日期：** {datetime.now().strftime('%Y-%m-%d')}")
        summary.append(f"**时间范围：** {self.config.get('since', 'daily')}")
        summary.append("")
        summary.append("## 🔥 热点项目")
        summary.append("")
        
        for i, trend in enumerate(trends[:10], 1):
            summary.append(f"### {i}. {trend['name']}")
            summary.append(f"- **描述：** {trend.get('description', 'N/A')}")
            summary.append(f"- **语言：** {trend.get('language', 'N/A')}")
            summary.append(f"- **Stars：** ⭐ {trend.get('stars', 0)}")
            summary.append(f"- **Forks：** 🍴 {trend.get('forks', 0)}")
            summary.append(f"- **链接：** [{trend['url']}]({trend['url']})")
            summary.append("")
        
        return '\n'.join(summary)
    
    def save_trends(self, trends: List[Dict]):
        """保存 trending 数据"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'trends': trends
        }
        
        with open(self.trends_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 数据已保存：{self.trends_file}")
    
    def load_history(self, days: int = 7) -> List[Dict]:
        """加载历史数据"""
        if not os.path.exists(self.trends_file):
            return []
        
        with open(self.trends_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('trends', [])
    
    def notify(self, summary: str):
        """
        发送通知
        
        Args:
            summary: 摘要内容
        """
        if not self.config.get('notify', True):
            return
        
        print("📬 发送通知...")
        # 简化实现 - 实际可集成飞书/钉钉/邮件等
        print(summary[:500] + "..." if len(summary) > 500 else summary)
    
    def run(self, auto_save: bool = True) -> str:
        """
        执行监控流程
        
        Args:
            auto_save: 是否自动保存
        
        Returns:
            str: 生成的摘要
        """
        print("🚀 开始 GitHub Trending 监控...")
        print("=" * 50)
        
        # 1. 获取 trending
        trends = self.fetch_trending(self.config.get('since', 'daily'))
        
        # 2. 过滤
        trends = self.filter_by_keywords(trends)
        trends = self.filter_by_language(trends)
        
        # 3. 生成摘要
        summary = self.generate_summary(trends)
        
        # 4. 保存
        if auto_save:
            self.save_trends(trends)
        
        # 5. 通知
        self.notify(summary)
        
        print("=" * 50)
        print("✅ 监控完成")
        
        return summary


def main():
    """命令行入口"""
    import sys
    
    monitor = GitHubTrendMonitor()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'config':
            # 显示配置
            print("当前配置:")
            print(json.dumps(monitor.config, ensure_ascii=False, indent=2))
        
        elif command == 'set':
            # 设置配置
            if len(sys.argv) < 4:
                print("用法：monitor.py set <key> <value>")
                sys.exit(1)
            key = sys.argv[2]
            value = sys.argv[3]
            monitor.config[key] = value
            monitor._save_config()
            print(f"✅ 配置已更新：{key} = {value}")
        
        elif command == 'history':
            # 显示历史
            history = monitor.load_history()
            print(f"历史数据：{len(history)} 条")
        
        else:
            print(f"未知命令：{command}")
    else:
        # 运行监控
        summary = monitor.run()
        print("\n" + summary)


if __name__ == '__main__':
    main()

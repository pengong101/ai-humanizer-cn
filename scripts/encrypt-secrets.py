#!/usr/bin/env python3
"""
敏感信息加密脚本
使用 Fernet 对称加密保护敏感配置

用法：
    python3 encrypt-secrets.py encrypt   # 加密
    python3 encrypt-secrets.py decrypt   # 解密
"""

import os
import sys
import json
from cryptography.fernet import Fernet

# 密钥文件路径
KEY_FILE = "/root/.openclaw/workspace/.secrets.key"
SECRETS_FILE = "/root/.openclaw/workspace/.env.secrets"
ENCRYPTED_FILE = "/root/.openclaw/workspace/.env.secrets.enc"


def generate_key():
    """生成加密密钥"""
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as f:
        f.write(key)
    os.chmod(KEY_FILE, 0o600)
    print(f"✅ 密钥已生成：{KEY_FILE}")
    print(f"⚠️  请安全保存此密钥，丢失后无法解密！")
    return key


def load_key():
    """加载加密密钥"""
    if not os.path.exists(KEY_FILE):
        print("❌ 密钥文件不存在，正在生成...")
        return generate_key()
    with open(KEY_FILE, 'rb') as f:
        return f.read()


def encrypt_secrets():
    """加密敏感信息"""
    if not os.path.exists(SECRETS_FILE):
        print(f"❌ 源文件不存在：{SECRETS_FILE}")
        sys.exit(1)
    
    key = load_key()
    f = Fernet(key)
    
    with open(SECRETS_FILE, 'rb') as file:
        data = file.read()
    
    encrypted = f.encrypt(data)
    
    with open(ENCRYPTED_FILE, 'wb') as file:
        file.write(encrypted)
    
    os.chmod(ENCRYPTED_FILE, 0o600)
    print(f"✅ 已加密：{ENCRYPTED_FILE}")
    print(f"🔒 原始文件已删除")
    os.remove(SECRETS_FILE)


def decrypt_secrets():
    """解密敏感信息"""
    if not os.path.exists(ENCRYPTED_FILE):
        print(f"❌ 加密文件不存在：{ENCRYPTED_FILE}")
        sys.exit(1)
    
    key = load_key()
    f = Fernet(key)
    
    with open(ENCRYPTED_FILE, 'rb') as file:
        encrypted = file.read()
    
    decrypted = f.decrypt(encrypted)
    
    with open(SECRETS_FILE, 'wb') as file:
        file.write(decrypted)
    
    os.chmod(SECRETS_FILE, 0o600)
    print(f"✅ 已解密：{SECRETS_FILE}")


def show_usage():
    """显示使用说明"""
    print("""
敏感信息加密工具

用法:
    python3 encrypt-secrets.py encrypt   # 加密 .env.secrets
    python3 encrypt-secrets.py decrypt   # 解密 .env.secrets.enc
    python3 encrypt-secrets.py keygen    # 重新生成密钥

文件说明:
    .env.secrets      - 明文敏感信息（使用后立即加密）
    .env.secrets.enc  - 加密后的敏感信息
    .secrets.key      - 加密密钥（权限 600）

安全建议:
    1. 密钥文件 .secrets.key 单独备份到安全位置
    2. 加密文件 .env.secrets.enc 可以安全提交到 Git
    3. 日常使用解密，修改后重新加密
    4. 定期更换密钥
""")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_usage()
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "encrypt":
        encrypt_secrets()
    elif action == "decrypt":
        decrypt_secrets()
    elif action == "keygen":
        if os.path.exists(KEY_FILE):
            print("⚠️  密钥已存在，是否覆盖？(y/N)")
            if input().lower() != 'y':
                sys.exit(0)
        generate_key()
    else:
        show_usage()
        sys.exit(1)

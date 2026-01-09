# 🌐 IP Scan Telegram Bot

A secure and permission-based Telegram bot that resolves a domain/URL to its IP address and performs **safe, fast port scans** using Nmap.  
Built for **educational, defensive security, and network diagnostics purposes**.

---

## 🚀 Features

- 🌍 Convert **domain / URL → IP address**
- 🔍 Perform **fast and non-intrusive port scans** (`nmap -F`)
- 🔐 **User whitelist** (only approved users can access the bot)
- ⏳ **Rate limiting** to prevent abuse
- 📱 Clean and readable Telegram responses
- 🧩 Works on **Termux** and **Linux VPS**
- ⚙️ Lightweight and easy to deploy

---

## 🧠 How It Works

1. User sends a command to the Telegram bot  
2. Bot resolves the domain to an IP address using DNS  
3. Bot performs a **safe port scan** on the IP  
4. Scan results are sent back to the user on Telegram

Version 2.0
dev by naif‑khaled
MADE IN SAUDI 🇸🇦

One tool to rule them all – HR Hunter, Instagram OSINT, TikTok Recon, Domain OSINT, Subdomain/Port Scanners, and Telegram Number Lookup – all in one powerful GUI & CLI.

📌 Overview
ΩMEGASCOUT is a professional, all‑in‑one OSINT (Open Source Intelligence) toolkit designed for security researchers, penetration testers, and ethical hackers. It brings together six independent OSINT modules into a single unified interface – both Graphical (PySide6) and Command‑Line.

The suite is built for speed, reliability, and depth of information gathering. It includes:

HR Email Hunter – discovers and verifies HR/recruiter email addresses for a given domain.

Instagram Viewer – fetches detailed public profile information using session cookies.

OSINT Pro – comprehensive domain reconnaissance (DNS, ports, HTTP headers, SSL, WAF, subdomains, emails, WHOIS, etc.).

TikTok Recon – extracts public TikTok profile data without authentication.

OmegaScout – advanced subdomain enumeration, port scanning, web fingerprinting, email harvesting, social media discovery, Wayback Machine, GitHub secret scanning, SSL analysis, Shodan/VirusTotal integration, and vulnerability checks.

Numberbook – phone number lookup via a Telegram bot (requires bot credentials).

✨ Features
🖥️ Dark Hacker GUI – built with PySide6, aggressive red/cyan theme, fully resizable.

🔥 Async & Multi‑threaded – fast scans using asyncio and ThreadPoolExecutor.

📊 Multiple Output Formats – JSON, CSV, HTML reports for all modules.

🧩 Modular Architecture – each tool can be run independently via CLI.

🔐 API Integrations – Hunter.io, Shodan, VirusTotal, GitHub (optional).

📱 Telegram Number Lookup – integrates with a Telegram bot for phone number info.

🌍 RTL Support – proper display of Arabic/right‑to‑left text (TikTok bios, etc.).

🏷️ Credits & Branding – proudly displays "dev by naif‑khaled" and "MADE IN SAUDI".

📦 Installation
1. Clone or download the script
Save the main script as A.py (or any name you like).

2. Install dependencies
bash
pip install pyside6 requests beautifulsoup4 dnspython aiohttp \
            python-whois shodan pyOpenSSL cryptography lxml \
            aiodns aiofile jinja2 telethon python-dotenv \
            rich tqdm colorama Pillow arabic-reshaper python-bidi
Note: Some modules (e.g., shodan) are optional; if you don't have API keys, the tool will skip those steps gracefully.

3. (Optional) Set up environment variables
For Numberbook, create a .env file in the same directory:

env
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
BOT_USERNAME=your_bot_username
For OmegaScout integrations, you can export:

bash
export VT_API_KEY="your_virustotal_key"
export SHODAN_API_KEY="your_shodan_key"
export GITHUB_TOKEN="your_github_token"
🚀 Usage
🖥️ GUI Mode (default)
bash
python A.py
This launches the PySide6 graphical interface with six tabs:

HR Hunter – input domain, optional Hunter API key, names, etc.

Instagram – enter session cookies (or load JSON) to fetch profile data.

OSINT Pro – select modules (DNS, ports, headers, etc.) and scan a domain.

TikTok – enter a username to retrieve public profile info.

OmegaScout – full‑spectrum domain scan (subdomains, ports, emails, etc.).

Numberbook – enter a phone number to query via Telegram bot.

🧪 CLI Mode (headless)
Each tool can be run from the terminal with its own arguments.

HR Email Hunter
bash
python A.py hr -d example.com -k YOUR_HUNTER_API_KEY -n "Jane Doe" -w 15 --export --report
Instagram Viewer
bash
python A.py insta --sessionid SESSION_COOKIE --csrftoken CSRF_COOKIE --userid USER_ID --target TARGET_USER
OSINT Pro
bash
python A.py osint --cli example.com --modules "DNS & Host" "Port Scan" "HTTP Headers"
(If --modules is omitted, all modules run.)

TikTok Recon
bash
python A.py tiktok --username tiktok_user
OmegaScout
bash
python A.py scout --domain example.com
Numberbook
bash
python A.py numberbook --phone +1234567890
📁 Output Files
All modules save reports to the scout_results/ directory (or current folder for OSINT Pro):

HR Hunter: hr_<domain>.csv, hr_<domain>.json, hr_<domain>.html

OSINT Pro: osint_<domain>_<timestamp>.json

OmegaScout: omegascout_report.json, omegascout_report.csv, omegascout_report.html

Instagram & TikTok: output is printed to the GUI or console; no files are saved by default.

⚙️ Configuration (API Keys)
Hunter.io: set via -k in CLI or GUI field.

Shodan: SHODAN_API_KEY environment variable.

VirusTotal: VT_API_KEY environment variable.

GitHub: GITHUB_TOKEN environment variable.

Telegram (Numberbook): .env file with TELEGRAM_API_ID, TELEGRAM_API_HASH, BOT_USERNAME.

⚠️ Disclaimer
ΩMEGASCOUT is intended for authorized security testing, educational purposes, and personal research only.
The author (naif‑khaled) and contributors are not responsible for any misuse or illegal activities performed with this tool. Always obtain proper written permission before scanning or testing any system or service. Respect privacy and applicable laws.

🙏 Credits
Developer: naif‑khaled

Country: Saudi Arabia 🇸🇦

Special thanks to the open‑source community for the amazing libraries that made this possible.

📄 License
This project is released under the Unlicense – you are free to use, modify, and distribute it without any restrictions. However, we encourage you to maintain the credits and the "MADE IN SAUDI" branding as a sign of respect to the author.

Happy OSINTing!
— naif‑khaled

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║   ██████╗ ███╗   ███╗███████╗ ██████╗  █████╗ ███████╗ ██████╗ ██████╗ ██╗   ██╗████████╗
║  ██╔═══██╗████╗ ████║██╔════╝██╔════╝ ██╔══██╗██╔════╝██╔═══██╗██╔══██╗██║   ██║╚══██╔══╝
║  ██║   ██║██╔████╔██║█████╗  ██║  ███╗███████║███████╗██║   ██║██████╔╝██║   ██║   ██║
║  ██║   ██║██║╚██╔╝██║██╔══╝  ██║   ██║██╔══██║╚════██║██║   ██║██╔══██╗██║   ██║   ██║
║  ╚██████╔╝██║ ╚═╝ ██║███████╗╚██████╔╝██║  ██║███████║╚██████╔╝██║  ██║╚██████╔╝   ██║
║   ╚═════╝ ╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝
║                                                                                        ║
║        UNIFIED OSINT SUITE  –  v2.0  –  dev by naif‑khaled                           ║
║   MADE IN SAUDI  🇸🇦                                                              ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

# ── ALL IMPORTS ─────────────────────────────────────────────────────────
import sys, os, re, json, csv, uuid, time, socket, smtplib, sqlite3, argparse
import threading, webbrowser, zlib, gzip, ssl, subprocess, queue, logging, io
import asyncio, random, hashlib, ipaddress
from datetime import datetime
from urllib.parse import urljoin, urlparse, quote
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Set, Any, Callable, Union
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum, auto
from collections import defaultdict, deque

import aiohttp, aiofiles, dns.resolver, dns.zone, whois
from bs4 import BeautifulSoup
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import OpenSSL, requests
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import TimeoutError

from PySide6.QtCore import Qt, QThread, Signal, QObject, QTimer, QCoreApplication, QEventLoop
from PySide6.QtGui import QFont, QPalette, QColor, QPixmap, QIcon, QAction, QPainter, QBrush, QPen, QLinearGradient, QGradient
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QGroupBox, QFormLayout, QMessageBox, QProgressBar, QFileDialog,
    QCheckBox, QScrollArea, QTabWidget, QSplitter, QTableWidget, QTableWidgetItem,
    QHeaderView, QComboBox, QSpinBox, QFrame, QStatusBar, QToolBar, QMenuBar,
    QMenu, QDialog, QDialogButtonBox, QGridLayout, QListWidget, QListWidgetItem,
    QAbstractItemView, QStyle, QStyleFactory
)

try:
    from rich.console import Console
    from rich.table import Table
    HAS_RICH = True
except:
    HAS_RICH = False

try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    HAS_BIDI = True
except:
    HAS_BIDI = False

# ── COMMON CONFIG ──────────────────────────────────────────────────────
VERSION = "2.0 UNIFIED"
EMAIL_RE = re.compile(r'[\w.\-+]+@[\w.\-]+\.[a-zA-Z]{2,}')
DB_PATH = "hr_cache.db"

DARK_STYLE = """
QMainWindow{background-color:#0a0a0f;}
QWidget{background-color:#0a0a0f;color:#e0e0e0;font-family:"Consolas","Courier New",monospace;}
QGroupBox{color:#00e5ff;border:1px solid #2a2a3a;border-radius:8px;margin-top:1ex;font-weight:bold;}
QGroupBox::title{subcontrol-origin:margin;left:10px;padding:0 5px 0 5px;color:#d32f2f;}
QLineEdit,QTextEdit,QPlainTextEdit,QSpinBox,QComboBox{background-color:#14141e;color:#e0e0e0;border:1px solid #2a2a3a;border-radius:4px;padding:5px;}
QLineEdit:focus,QTextEdit:focus,QSpinBox:focus,QComboBox:focus{border:1px solid #d32f2f;}
QPushButton{background-color:#d32f2f;color:#000;border:none;border-radius:4px;padding:8px 16px;font-weight:bold;}
QPushButton:hover{background-color:#b71c1c;} QPushButton:pressed{background-color:#880e0e;}
QPushButton:disabled{background-color:#2a2a3a;color:#7a7a8a;}
QProgressBar{background-color:#14141e;border:1px solid #2a2a3a;border-radius:4px;text-align:center;color:#e0e0e0;}
QProgressBar::chunk{background-color:#d32f2f;border-radius:4px;}
QTabWidget::pane{border:1px solid #2a2a3a;background:#0a0a0f;}
QTabBar::tab{background:#14141e;color:#7a7a8a;padding:8px 16px;margin-right:2px;border-top-left-radius:4px;border-top-right-radius:4px;}
QTabBar::tab:selected{background:#0a0a0f;color:#00e5ff;} QTabBar::tab:hover{background:#2a2a3a;}
QTableWidget{background-color:#14141e;alternate-background-color:#2a2a3a;gridline-color:#2a2a3a;}
QHeaderView::section{background-color:#2a2a3a;color:#7a7a8a;padding:4px;}
QStatusBar{background-color:#14141e;color:#7a7a8a;}
QScrollBar:vertical{background:#0a0a0f;width:12px;margin:0px;}
QScrollBar::handle:vertical{background:#2a2a3a;min-height:20px;border-radius:6px;}
QScrollBar::handle:vertical:hover{background:#00e5ff;}
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{border:none;background:none;}
QLabel#logo_label{font-size:22px;font-weight:bold;color:#d32f2f;background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #0a0a0f,stop:0.3 #1a1010,stop:0.7 #1a1010,stop:1 #0a0a0f);border-bottom:3px solid #d32f2f;padding:15px;margin:0;}
"""

def fix_rtl(text):
    if not text:
        return ""
    if HAS_BIDI and any(ord(c) > 127 for c in text):
        try:
            return get_display(arabic_reshaper.reshape(text))
        except:
            pass
    return text

# ══════════════════════════════════════════════════════════════════════
#  HR EMAIL HUNTER
# ══════════════════════════════════════════════════════════════════════
class Cache:
    def __init__(self, path=DB_PATH):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self._setup()

    def _setup(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS results (
                email TEXT PRIMARY KEY,
                domain TEXT,
                status TEXT,
                score INTEGER,
                sources TEXT,
                ts TEXT
            )
        """)
        self.conn.commit()

    def get(self, email):
        row = self.conn.execute("SELECT * FROM results WHERE email=?", (email,)).fetchone()
        if row:
            return {
                "email": row[0],
                "domain": row[1],
                "status": row[2],
                "score": row[3],
                "sources": json.loads(row[4]),
                "ts": row[5]
            }
        return None

    def save(self, email, domain, status, score, sources):
        self.conn.execute(
            "INSERT OR REPLACE INTO results VALUES (?,?,?,?,?,?)",
            (email, domain, status, score, json.dumps(sources), datetime.now().isoformat())
        )
        self.conn.commit()

    def all_for_domain(self, domain):
        rows = self.conn.execute("SELECT * FROM results WHERE domain=?", (domain,)).fetchall()
        return [
            {
                "email": r[0],
                "status": r[2],
                "score": r[3],
                "sources": json.loads(r[4])
            }
            for r in rows
        ]

HR_ALIASES = [
    "hr", "careers", "recruitment", "jobs", "talent", "hiring", "recruiter",
    "humanresources", "hrdept", "staffing", "people", "talentacquisition",
    "career", "joinus", "workwithus", "hrteam", "peopleops", "peopleandculture",
    "talentteam", "hrbp", "talentpartner", "recruiting", "hroffice", "peopleteam",
    "hradmin", "hrmail", "careerservice", "employer", "recruit", "apply",
    "opportunities", "work", "join", "hq", "contact", "info", "hello", "team",
    "office", "admin", "general", "enquiries", "jobseekers", "hiringteam",
    "hr.team", "talent.team", "people.team", "careers.team"
]

CRAWL_PATHS = [
    "/", "/contact", "/contact-us", "/about", "/about-us", "/team",
    "/our-team", "/careers", "/jobs", "/work-with-us", "/join-us",
    "/people", "/hr", "/company", "/meet-the-team", "/who-we-are",
    "/hire", "/hiring", "/apply"
]

NAME_FORMATS = [
    "{first}.{last}", "{f}.{last}", "{first}{last}", "{first}_{last}",
    "{last}.{first}", "{f}{last}", "{first}.{l}", "{first}",
    "{last}", "{f}_{last}", "{first}-{last}", "{f}-{last}",
    "{last}{f}", "{last}{first}", "{first}{l}"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

class WebsiteCrawler:
    FALSE_POSITIVES = {"example.com", "sentry.io", "schema.org", "w3.org", ".png", ".jpg", ".svg", "noreply", "no-reply"}

    def __init__(self, domain, timeout=10):
        self.domain = domain
        self.timeout = timeout

    def _crawl_one(self, url):
        emails = set()
        try:
            r = requests.get(url, headers=HEADERS, timeout=self.timeout, allow_redirects=True)
            if r.status_code != 200:
                return emails
            for m in EMAIL_RE.findall(r.text):
                m = m.lower().strip(".,;")
                if any(fp in m for fp in self.FALSE_POSITIVES):
                    continue
                emails.add(m)
            soup = BeautifulSoup(r.text, "html.parser")
            for tag in soup.find_all("a", href=True):
                href = tag["href"]
                if href.startswith("mailto:"):
                    em = href[7:].split("?")[0].lower().strip()
                    if em and "@" in em:
                        emails.add(em)
        except:
            pass
        return emails

    def crawl(self, workers=10):
        urls = []
        for proto in ("https", "http"):
            for path in CRAWL_PATHS:
                urls.append(f"{proto}://{self.domain}{path}")
        all_found = {}
        company_part = self.domain.split(".")[-2]
        with ThreadPoolExecutor(max_workers=workers) as ex:
            fmap = {ex.submit(self._crawl_one, u): u for u in urls}
            for future in as_completed(fmap):
                url = fmap[future]
                for email in future.result():
                    if company_part in email:
                        if email not in all_found:
                            all_found[email] = set()
                        all_found[email].add(url)
        return {e: sorted(pages) for e, pages in all_found.items()}

class O365Checker:
    URL = "https://login.microsoftonline.com/common/GetCredentialType"

    @classmethod
    def check(cls, email):
        try:
            r = requests.post(
                cls.URL,
                headers={"Content-Type": "application/json"},
                json={"Username": email},
                timeout=7
            )
            return r.json().get("IfExistsResult") == 0
        except:
            return False

    @classmethod
    def bulk(cls, emails, workers=12, progress_cb=None):
        out = []
        with ThreadPoolExecutor(max_workers=workers) as ex:
            fmap = {ex.submit(cls.check, e): e for e in emails}
            for future in as_completed(fmap):
                email = fmap[future]
                try:
                    valid = future.result()
                except:
                    valid = False
                out.append({
                    "email": email,
                    "valid": valid,
                    "status": "valid" if valid else "invalid",
                    "method": "O365"
                })
                if progress_cb:
                    progress_cb(email, valid)
        return out

class SMTPVerifier:
    def __init__(self, mx_records):
        self.mx = mx_records
        self.catchall = False

    def _probe(self, email):
        for mx in self.mx[:1]:
            try:
                s = smtplib.SMTP(mx, 25, timeout=7)
                s.ehlo_or_helo_if_needed()
                s.mail("probe@example.com")
                code, _ = s.rcpt(email)
                s.quit()
                if code in (250, 251):
                    return "valid"
                if code in (550, 553, 554):
                    return "invalid"
                return "unknown"
            except (socket.timeout, ConnectionRefusedError, smtplib.SMTPServerDisconnected):
                return "timeout"
            except:
                return "error"
        return "error"

    def detect_catchall(self, domain):
        test = f"{uuid.uuid4().hex[:10]}@{domain}"
        self.catchall = (self._probe(test) == "valid")
        return self.catchall

    def bulk(self, emails, workers=12, progress_cb=None):
        if self.catchall:
            return [
                {"email": e, "valid": None, "status": "catch_all", "method": "SMTP"}
                for e in emails
            ]
        out = []
        with ThreadPoolExecutor(max_workers=workers) as ex:
            fmap = {ex.submit(self._probe, e): e for e in emails}
            for future in as_completed(fmap):
                email = fmap[future]
                try:
                    status = future.result()
                except:
                    status = "error"
                valid = (status == "valid")
                out.append({
                    "email": email,
                    "valid": valid,
                    "status": status,
                    "method": "SMTP"
                })
                if progress_cb:
                    progress_cb(email, valid)
        return out

class HunterAPI:
    BASE = "https://api.hunter.io/v2"

    def __init__(self, key, domain):
        self.key = key
        self.domain = domain

    def search(self):
        try:
            r = requests.get(
                f"{self.BASE}/domain-search",
                params={"domain": self.domain, "api_key": self.key},
                timeout=15
            )
            d = r.json().get("data", {})
            return {
                "pattern": d.get("pattern"),
                "emails": [
                    {
                        "email": e["value"],
                        "confidence": e.get("confidence", 0),
                        "type": e.get("type", "?")
                    }
                    for e in d.get("emails", [])
                ]
            }
        except Exception as e:
            return {"error": str(e)}

class EmailGenerator:
    @staticmethod
    def aliases(domain):
        return [f"{a}@{domain}" for a in HR_ALIASES]

    @staticmethod
    def from_names(names, domain, pattern=None):
        out = set()
        for full in names:
            parts = full.strip().lower().split()
            if len(parts) < 2:
                continue
            first, last = parts[0], parts[-1]
            f, l = first[0], last[0]
            ctx = {"first": first, "last": last, "f": f, "l": l}
            if pattern:
                try:
                    out.add(f"{pattern.format(**ctx)}@{domain}")
                except:
                    pass
            for fmt in NAME_FORMATS:
                try:
                    out.add(f"{fmt.format(**ctx)}@{domain}")
                except:
                    pass
        return list(out)

def score_email(email, sources, verified, hunter_conf=0):
    s = 0
    if verified:
        s += 50
    if "website" in sources:
        s += 20
    if "hunter" in sources:
        s += 15
    if "social" in sources:
        s += 10
    if hunter_conf:
        s += min(hunter_conf // 10, 5)
    if "o365" in sources and verified:
        s += 5
    local = email.split("@")[0]
    if local in ("info", "hello", "contact", "admin", "general"):
        s = max(s - 10, 0)
    return min(s, 100)

def generate_html_report(domain, results, social, hunter_data, is_outlook, website_emails, elapsed):
    return "<html><body>Report</body></html>"

def hr_run(args, log_cb=None):
    domain = args.domain
    hunter_key = getattr(args, 'hunter_key', None)
    names = getattr(args, 'names', []) or []
    workers = getattr(args, 'workers', 15)
    export = getattr(args, 'export', True)
    report = getattr(args, 'report', True)

    if log_cb:
        log_cb(f"Starting HR scan on {domain}")

    all_emails = {}
    sources_dict = defaultdict(list)

    if log_cb:
        log_cb("Crawling website...")
    crawler = WebsiteCrawler(domain)
    web_emails = crawler.crawl(workers)
    for email, pages in web_emails.items():
        all_emails[email] = True
        sources_dict[email].append("website")

    if log_cb:
        log_cb("Generating aliases...")
    for email in EmailGenerator.aliases(domain):
        all_emails[email] = True
        sources_dict[email].append("alias")

    if names:
        if log_cb:
            log_cb(f"Generating from {len(names)} names...")
        for email in EmailGenerator.from_names(names, domain):
            all_emails[email] = True
            sources_dict[email].append("names")

    if hunter_key:
        if log_cb:
            log_cb("Querying Hunter.io...")
        hunter = HunterAPI(hunter_key, domain)
        data = hunter.search()
        if "emails" in data:
            for e in data["emails"]:
                email = e["email"]
                all_emails[email] = True
                sources_dict[email].append("hunter")

    emails_list = list(all_emails.keys())
    if log_cb:
        log_cb(f"Verifying {len(emails_list)} emails...")

    o365_results = O365Checker.bulk(emails_list, workers, progress_cb=log_cb)
    o365_valid = {r["email"]: r["valid"] for r in o365_results}

    try:
        mx_records = [str(r.exchange) for r in dns.resolver.resolve(domain, 'MX')]
    except:
        mx_records = []

    smtp_valid = {}
    if mx_records:
        verifier = SMTPVerifier(mx_records)
        verifier.detect_catchall(domain)
        smtp_results = verifier.bulk(emails_list, workers, progress_cb=log_cb)
        smtp_valid = {r["email"]: r["valid"] for r in smtp_results}

    final = []
    for email in emails_list:
        valid = o365_valid.get(email, False) or smtp_valid.get(email, False)
        if o365_valid.get(email) is False and smtp_valid.get(email) is True:
            valid = True
        sources = sources_dict.get(email, [])
        score = score_email(email, sources, valid, 0)
        final.append({
            "email": email,
            "valid": valid,
            "score": score,
            "sources": sources,
            "status": "valid" if valid else "invalid"
        })

    final.sort(key=lambda x: (x["valid"], x["score"]), reverse=True)

    if log_cb:
        log_cb(f"Scan complete. Found {len(final)} emails, {sum(1 for f in final if f['valid'])} valid.")

    if export:
        out_dir = "scout_results"
        os.makedirs(out_dir, exist_ok=True)
        csv_path = os.path.join(out_dir, f"hr_{domain}.csv")
        json_path = os.path.join(out_dir, f"hr_{domain}.json")
        with open(csv_path, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=["email", "valid", "score", "sources", "status"])
            w.writeheader()
            w.writerows(final)
        with open(json_path, 'w') as f:
            json.dump(final, f, indent=2, default=str)
        if log_cb:
            log_cb(f"CSV saved to {csv_path}, JSON to {json_path}")

    if report:
        out_dir = "scout_results"
        os.makedirs(out_dir, exist_ok=True)
        html_path = os.path.join(out_dir, f"hr_{domain}.html")
        with open(html_path, 'w') as f:
            f.write(generate_html_report(domain, final, [], {}, False, {}, 0))
        if log_cb:
            log_cb(f"HTML report saved to {html_path}")

    return final

# ══════════════════════════════════════════════════════════════════════
#  INSTAGRAM VIEWER
# ══════════════════════════════════════════════════════════════════════
def print_profile_text(info):
    lines = []
    lines.append("=" * 70)
    lines.append(f"👤 @{info.get('username', 'N/A')} ({info.get('full_name', 'N/A')})")
    lines.append("=" * 70)
    lines.append(f"🆔 User ID         : {info.get('id', 'N/A')}")
    lines.append(f"🔒 Private         : {'YES' if info.get('is_private') else 'NO'}")
    lines.append(f"✅ Verified        : {'YES' if info.get('is_verified') else 'NO'}")
    acc_type = info.get('professional_type') or 'Personal'
    if info.get('is_business'):
        acc_type += ' (Business)'
    elif info.get('is_professional'):
        acc_type += ' (Creator)'
    else:
        acc_type += ' (Personal)'
    lines.append(f"📊 Account type    : {acc_type}")
    if info.get('business_category'):
        lines.append(f"🏢 Category        : {info['business_category']}")
    if info.get('business_email'):
        lines.append(f"📧 Email           : {info['business_email']}")
    if info.get('business_phone'):
        lines.append(f"📞 Phone           : {info['business_phone']}")
    if info.get('address_street') or info.get('city'):
        street = info.get('address_street', '')
        city = info.get('city', '')
        zip_code = info.get('zip', '')
        lines.append(f"📍 Address         : {street}, {city} {zip_code}".strip())
    lines.append(f"\n👥 Followers       : {info.get('follower_count', 0):,}")
    lines.append(f"👣 Following       : {info.get('following_count', 0):,}")
    lines.append(f"📷 Posts           : {info.get('post_count', 0):,}")
    lines.append(f"🎬 Reels           : {info.get('reel_count', 0)}")
    lines.append(f"📺 IGTV            : {info.get('igtv_count', 0)}")
    lines.append(f"⭐ Highlights      : {info.get('highlight_count', 0)}")
    bio = info.get('bio', '')[:200]
    lines.append(f"\n📝 Bio             : {bio}")
    bio_links = info.get('bio_links', [])
    if bio_links:
        links = [l.get('url', '') for l in bio_links if l.get('url')]
        if links:
            lines.append(f"🔗 Bio links       : {', '.join(links)}")
    if info.get('external_url'):
        lines.append(f"🌐 External URL   : {info['external_url']}")
    if info.get('profile_pic_url'):
        lines.append(f"🖼️ Profile pic URL : {info['profile_pic_url'][:80]}...")
    if info.get('joined_recently'):
        lines.append("🆕 Joined recently")
    lines.append(f"\n🤝 You follow them : {info.get('following_viewer', False)}")
    lines.append(f"🤝 They follow you : {info.get('followed_by_viewer', False)}")
    lines.append("=" * 70)
    return "\n".join(lines)

def get_own_username_from_homepage(session):
    try:
        resp = session.get('https://www.instagram.com/', timeout=10)
        if resp.status_code != 200:
            return None
        match = re.search(r'window\._sharedData\s*=\s*({.*?});', resp.text, re.DOTALL)
        if not match:
            return None
        shared = json.loads(match.group(1))
        viewer = shared.get('config', {}).get('viewer')
        if viewer and viewer.get('username'):
            return viewer['username']
        return None
    except:
        return None

def fetch_profile(sessionid, csrftoken, user_id, target_username=None, retry_count=3, status_callback=None):
    for attempt in range(retry_count + 1):
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15',
            'Accept': 'application/json, text/plain, */*',
            'X-IG-App-ID': '936619743392459',
        })
        session.cookies.set('sessionid', sessionid, domain='.instagram.com')
        session.cookies.set('csrftoken', csrftoken, domain='.instagram.com')
        session.headers['X-CSRFToken'] = csrftoken

        try:
            r = session.get('https://www.instagram.com/', timeout=5)
            match = re.search(r'"www_claim":"([^"]+)"', r.text)
            if match:
                session.headers['X-IG-WWW-Claim'] = match.group(1)
        except:
            pass

        if not target_username:
            info_url = f'https://i.instagram.com/api/v1/users/{user_id}/info/'
            resp = session.get(info_url, params={'__d': 'disco', '__user': user_id}, timeout=10)
            if resp.status_code == 200:
                try:
                    target_username = resp.json().get('user', {}).get('username')
                except:
                    pass
            if not target_username:
                target_username = get_own_username_from_homepage(session)
                if not target_username:
                    return {'error': 'Could not auto-detect your username.'}

        web_url = 'https://i.instagram.com/api/v1/users/web_profile_info/'
        params = {
            'username': target_username,
            '__d': 'disco',
            '__user': user_id,
            '__a': '1',
            '__req': '3',
        }
        resp = session.get(web_url, params=params, timeout=10)

        if resp.status_code == 200:
            try:
                data = resp.json()
                user_data = data.get('data', {}).get('user') or data.get('user')
                if not user_data:
                    return {'error': 'User data not found.'}
                profile = {
                    'id': user_data.get('id'),
                    'username': user_data.get('username'),
                    'full_name': user_data.get('full_name'),
                    'is_private': user_data.get('is_private'),
                    'is_verified': user_data.get('is_verified'),
                    'professional_type': user_data.get('professional_type'),
                    'is_business': user_data.get('is_business'),
                    'is_professional': user_data.get('is_professional'),
                    'business_category': user_data.get('business_category'),
                    'business_email': user_data.get('business_email'),
                    'business_phone': user_data.get('business_phone'),
                    'address_street': user_data.get('address_street'),
                    'city': user_data.get('city'),
                    'zip': user_data.get('zip'),
                    'follower_count': user_data.get('edge_followed_by', {}).get('count') or user_data.get('follower_count', 0),
                    'following_count': user_data.get('edge_follow', {}).get('count') or user_data.get('following_count', 0),
                    'post_count': user_data.get('edge_owner_to_timeline_media', {}).get('count') or user_data.get('media_count', 0),
                    'reel_count': user_data.get('reel_count', 0),
                    'igtv_count': user_data.get('igtv_count', 0),
                    'highlight_count': user_data.get('highlight_count', 0),
                    'bio': user_data.get('biography'),
                    'bio_links': user_data.get('bio_links'),
                    'external_url': user_data.get('external_url'),
                    'profile_pic_url': user_data.get('profile_pic_url'),
                    'joined_recently': user_data.get('joined_recently'),
                    'following_viewer': user_data.get('following_viewer'),
                    'followed_by_viewer': user_data.get('followed_by_viewer'),
                }
                return {'success': True, 'profile': profile}
            except Exception as e:
                return {'error': f'Parsing error: {e}'}

        elif resp.status_code == 429:
            retry_after = resp.headers.get('Retry-After')
            if retry_after and retry_after.isdigit():
                wait = int(retry_after)
            else:
                wait = 60 * (attempt + 1)
            if status_callback:
                status_callback(f"⚠️ Rate limited (attempt {attempt+1}). Waiting {wait}s...")
            if attempt < retry_count:
                time.sleep(wait)
                continue
            else:
                return {'error': f'Rate limited after {retry_count+1} attempts.'}
        else:
            return {'error': f'HTTP {resp.status_code}: {resp.text[:200]}'}

    return {'error': 'Unexpected failure.'}

# ══════════════════════════════════════════════════════════════════════
#  OSINT PRO
# ══════════════════════════════════════════════════════════════════════
import urllib.request
import urllib.error

_CHROME_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

def _decode_body(resp, raw):
    enc = (resp.headers.get("Content-Encoding") or "").lower()
    try:
        if enc == "gzip":
            raw = gzip.decompress(raw)
        elif enc == "deflate":
            try:
                raw = zlib.decompress(raw)
            except zlib.error:
                raw = zlib.decompress(raw, -zlib.MAX_WBITS)
    except:
        pass
    return raw.decode("utf-8", errors="ignore")

def _ssl_ctx(strict=False):
    ctx = ssl.create_default_context()
    if not strict:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    return ctx

def fetch(url, timeout=14, retries=2, extra_headers=None):
    headers = {**_CHROME_HEADERS, **(extra_headers or {})}
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=_ssl_ctx()))
    last_exc = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=headers)
            with opener.open(req, timeout=timeout) as r:
                raw = r.read()
                body = _decode_body(r, raw)
                return r, body, dict(r.headers)
        except Exception as exc:
            last_exc = exc
            if attempt < retries:
                time.sleep(1.2 * (attempt + 1))
    raise last_exc

def dns_host(domain):
    result = {}
    for typ in ('A', 'MX', 'NS', 'TXT'):
        try:
            result[typ] = [str(r) for r in dns.resolver.resolve(domain, typ)]
        except:
            pass
    return result

def port_scan(domain):
    open_ports = []
    common = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445,
              993, 995, 1723, 3306, 3389, 5432, 5900, 6379, 8080, 8443,
              9200, 27017]
    try:
        ip = socket.gethostbyname(domain)
        for port in common:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                if s.connect_ex((ip, port)) == 0:
                    open_ports.append(port)
                s.close()
            except:
                pass
    except:
        pass
    return {"open_ports": open_ports}

def http_headers(domain):
    try:
        r, body, headers = fetch(f"https://{domain}", timeout=10)
        return {"status": r.status, "headers": dict(headers)}
    except Exception as e:
        return {"error": str(e)}

def ssl_tls(domain):
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                return {
                    "subject": dict(cert['subject'][0]),
                    "issuer": dict(cert['issuer'][0]),
                    "notBefore": cert['notBefore'],
                    "notAfter": cert['notAfter']
                }
    except Exception as e:
        return {"error": str(e)}

def detect_waf(domain):
    return {"detected": []}

def detect_aws(domain):
    return {"aws_services": {}}

def detect_cloudflare(domain):
    return {"cloudflare": False}

def detect_nginx(domain):
    return {"server": "unknown"}

def subdomains(domain):
    try:
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            subs = set()
            for entry in data:
                name = entry.get('name_value', '')
                if name.endswith(domain):
                    subs.add(name.replace('*.', ''))
            return {"ct_log": list(subs), "brute_force": []}
    except:
        pass
    return {"ct_log": [], "brute_force": []}

def harvest(domain):
    emails = set()
    external = set()
    social = {}
    try:
        r, body, _ = fetch(f"https://{domain}", timeout=10)
        for m in EMAIL_RE.findall(body):
            emails.add(m)
        soup = BeautifulSoup(body, 'html.parser')
        for a in soup.find_all('a', href=True):
            h = a['href']
            if 'twitter.com' in h:
                social['twitter'] = h
            elif 'facebook.com' in h:
                social['facebook'] = h
            elif 'instagram.com' in h:
                social['instagram'] = h
            elif 'linkedin.com' in h:
                social['linkedin'] = h
            elif 'github.com' in h:
                social['github'] = h
    except:
        pass
    return {
        "emails": list(emails),
        "external_domains": list(external),
        "social_media": social
    }

def whois_info(domain):
    try:
        w = whois.whois(domain)
        return {
            "registrar": w.registrar,
            "creation_date": str(w.creation_date),
            "expiration_date": str(w.expiration_date)
        }
    except Exception as e:
        return {"error": str(e)}

def robots_sitemap(domain):
    found = []
    for path in ['/robots.txt', '/sitemap.xml']:
        try:
            url = f"https://{domain}{path}"
            r, body, _ = fetch(url, timeout=5)
            if r.status == 200:
                found.append(url)
        except:
            pass
    return {"found": found}

MODULES = [
    ("DNS & Host", dns_host),
    ("Port Scan", port_scan),
    ("HTTP Headers", http_headers),
    ("SSL / TLS", ssl_tls),
    ("WAF Detection", detect_waf),
    ("AWS Detection", detect_aws),
    ("Cloudflare", detect_cloudflare),
    ("Web Server", detect_nginx),
    ("Subdomains", subdomains),
    ("Emails & Links", harvest),
    ("WHOIS", whois_info),
    ("Robots & Sitemap", robots_sitemap),
]

MODULE_MAP = dict(MODULES)

def save_results(domain, results, filepath=None):
    if not filepath:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"osint_{domain.replace('.', '_')}_{ts}.json"
    out = Path(filepath)
    payload = {
        "meta": {
            "target": domain,
            "tool": "OSINT Pro v4.0",
            "scan_time": datetime.now().isoformat()
        },
        "results": results
    }
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    return out

# ══════════════════════════════════════════════════════════════════════
#  TIKTOK RECON
# ══════════════════════════════════════════════════════════════════════
TIKTOK_COOKIES = {
    "sessionid": "0f836a0c35ae256ce359f71eb8e106c0",
    "tt_csrf_token": "v3TmNqIa-6gkY4odaOcDjcU0dyWbQdgM1-_Y",
    "ttwid": "1%7Crrr2tGZ_WvxZePAga-WviFIijTG5O0-uMOSvnSDBtDg%7C1782086758%7C61002380b9f0ec76d7711d4bce09e4ddd0f02ad156e0c13bd08a57604d98969f",
    "s_v_web_id": "verify_mqoez0pg_l7Wpj1dV_aslQ_4euL_AZYX_nrjWyN14YbrD"
}
_TT_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

def deep_find(obj, target_key=None, target_value=None):
    if isinstance(obj, dict):
        if target_key and target_key in obj:
            return obj
        if target_value is not None:
            for v in obj.values():
                if v == target_value:
                    return obj
        for v in obj.values():
            res = deep_find(v, target_key, target_value)
            if res:
                return res
    elif isinstance(obj, list):
        for item in obj:
            res = deep_find(item, target_key, target_value)
            if res:
                return res
    return None

def find_master_user(payload, username):
    clean = username.lower().lstrip("@")
    candidates = []

    def traverse(obj):
        if isinstance(obj, dict):
            uid = obj.get("uniqueId") or obj.get("unique_id") or ""
            if str(uid).lower() == clean:
                candidates.append(obj)
            for v in obj.values():
                traverse(v)
        elif isinstance(obj, list):
            for i in obj:
                traverse(i)

    try:
        usr = payload["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]["user"]
        if usr.get("uniqueId", "").lower() == clean:
            candidates.append(usr)
    except:
        pass

    traverse(payload)
    return max(candidates, key=len) if candidates else None

def get_profile_data(username):
    username = username.lstrip("@")
    url = f"https://www.tiktok.com/@{username}"
    headers = {
        "User-Agent": _TT_UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": "; ".join(f"{k}={v}" for k, v in TIKTOK_COOKIES.items())
    }

    try:
        resp = requests.get(url, headers=headers, timeout=15)
    except Exception as exc:
        return {"error": f"Connection failed: {exc}"}

    if resp.status_code != 200:
        return {"error": f"HTTP {resp.status_code} from TikTok"}

    match = re.search(
        r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>',
        resp.text, re.DOTALL
    )
    if not match:
        return {"error": "Rehydration script not found"}

    raw = match.group(1).strip()
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        try:
            payload = json.loads(re.sub(r"[\x00-\x1f]", "", raw))
        except Exception as exc:
            return {"error": f"JSON parse failed: {exc}"}

    user_obj = find_master_user(payload, username)
    if not user_obj:
        return {"error": f"No user object found for @{username}"}

    stats = deep_find(payload, target_key="followerCount") or user_obj.get("stats", {})
    region = (
        user_obj.get("region") or
        user_obj.get("iso_country_code") or
        user_obj.get("country") or
        user_obj.get("location") or
        user_obj.get("regionCode") or
        user_obj.get("language") or
        "UNKNOWN"
    )

    return {
        "user_id": user_obj.get("id"),
        "unique_id": user_obj.get("uniqueId"),
        "nickname": user_obj.get("nickname"),
        "bio": user_obj.get("bioDescription") or user_obj.get("signature"),
        "avatar": user_obj.get("avatarLarger") or user_obj.get("avatarMedium") or user_obj.get("avatarThumb"),
        "follower_count": stats.get("followerCount"),
        "following_count": stats.get("followingCount"),
        "heart_count": stats.get("heartCount"),
        "video_count": stats.get("videoCount"),
        "digg_count": stats.get("diggCount"),
        "is_verified": user_obj.get("verified", False),
        "is_private": user_obj.get("privateAccount", False),
        "region": region,
        "created": user_obj.get("createTime"),
    }

# ══════════════════════════════════════════════════════════════════════
#  OMEGASCOUT
# ══════════════════════════════════════════════════════════════════════
class Config:
    THREADS = 50
    TIMEOUT = 10
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    MAX_RETRIES = 3
    DELAY_BASE = 0.5
    DELAY_JITTER = 0.3

    SUBDOMAIN_WORDLIST = [
        "www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1", "webdisk",
        "ns2", "cpanel", "whm", "autodiscover", "autoconfig", "m", "imap", "test",
        "ns", "blog", "pop3", "dev", "www2", "admin", "forum", "news", "vpn", "ns3",
        "mail2", "new", "mysql", "old", "lists", "support", "mobile", "mx", "static",
        "docs", "beta", "shop", "sql", "secure", "demo", "cp", "calendar", "wiki",
        "web", "media", "email", "images", "img", "download", "dns", "piwik", "stats",
        "dashboard", "portal", "manage", "start", "help", "js", "css", "assets",
        "cdn", "files", "video", "music", "api", "app", "storage", "backup",
        "mirror", "owa", "exchange", "remote", "git", "svn", "jenkins", "jira",
        "confluence", "bitbucket", "sonar", "kibana", "elastic", "grafana",
        "prometheus", "alertmanager", "kafka", "zookeeper", "hadoop", "spark",
        "hive", "hbase", "yarn", "mesos", "marathon", "chronos", "cassandra",
        "mongo", "redis", "memcached", "rabbitmq", "activemq", "consul", "vault",
        "nomad", "terraform", "packer", "vagrant", "ansible", "puppet", "chef",
        "salt", "kubernetes", "k8s", "docker", "registry", "harbor", "nexus",
        "artifactory", "jenkins", "teamcity", "bamboo", "cruisecontrol", "sonatype",
        "auth", "oauth", "sso", "login", "signin", "register", "profile", "account"
    ]

    DIR_WORDLIST = [
        "admin", "login", "wp-admin", "administrator", "phpmyadmin", "mysql",
        "backup", "backups", "tmp", "temp", "logs", "config", "conf", "etc",
        "db", "database", "data", "assets", "uploads", "downloads", "files",
        "img", "images", "css", "js", "javascript", "scripts", "includes",
        "lib", "vendor", "node_modules", "bower_components", "dist", "build",
        "api", "v1", "v2", "api/v1", "api/v2", "rest", "restapi", "graphql",
        "swagger", "docs", "documentation", "help", "support", "contact",
        "about", "team", "careers", "jobs", "news", "blog", "events",
        "shop", "store", "cart", "checkout", "payment", "pay", "order",
        "track", "account", "user", "users", "profile", "settings", "edit",
        "register", "signup", "signin", "login", "logout", "forgot", "reset",
        "change", "password", "passwd", "secret", "private", "internal",
        "cgi-bin", "cgi", "cgi-bin/admin", "cgi-bin/php", "cgi-bin/perl",
        "icons", "favicon.ico", "robots.txt", "sitemap.xml", "sitemap.xml.gz",
        "crossdomain.xml", "clientaccesspolicy.xml", ".htaccess", ".htpasswd",
        "web.config", ".env", ".git", ".svn", ".hg", ".idea", ".vscode",
        ".DS_Store", "Thumbs.db", "desktop.ini", "index.html", "index.php",
        "default.html", "default.aspx", "home.html", "home.php", "main.html"
    ]

    VIRUSTOTAL_API_KEY = os.environ.get("VT_API_KEY", "")
    SHODAN_API_KEY = os.environ.get("SHODAN_API_KEY", "")
    OTX_API_KEY = os.environ.get("OTX_API_KEY", "")
    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

    OUTPUT_DIR = "scout_results"
    JSON_REPORT = f"{OUTPUT_DIR}/omegascout_report.json"
    CSV_REPORT = f"{OUTPUT_DIR}/omegascout_report.csv"
    HTML_REPORT = f"{OUTPUT_DIR}/omegascout_report.html"

class Target:
    def __init__(self, domain):
        self.domain = domain.lower()
        self.base_url = f"https://{domain}" if not domain.startswith("http") else domain
        self.parsed = urlparse(self.base_url)
        self.root_domain = self.parsed.netloc
        self.ip_addresses = []
        self.subdomains = set()
        self.open_ports = {}
        self.web_technologies = {}
        self.emails = set()
        self.social_handles = {}
        self.dns_records = {}
        self.whois_info = {}
        self.ssl_cert = {}
        self.wayback_urls = []
        self.dork_results = []
        self.github_secrets = []
        self.vulnerabilities = []
        self.directories_found = []
        self.shodan_info = {}
        self.virustotal_info = {}
        self.csp_headers = {}
        self.cookies = {}

logger_scout = logging.getLogger("OmegaScout")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def fetch_url(session, url, method='GET', data=None, headers=None, timeout=Config.TIMEOUT):
    if headers is None:
        headers = {'User-Agent': Config.USER_AGENT}
    for _ in range(Config.MAX_RETRIES):
        try:
            async with session.request(
                method, url,
                headers=headers,
                data=data,
                timeout=aiohttp.ClientTimeout(total=timeout),
                ssl=False
            ) as resp:
                body = await resp.read()
                return resp, body
        except (aiohttp.ClientError, asyncio.TimeoutError):
            await asyncio.sleep(random.uniform(0.5, 1.5))
    return None, b''

async def resolve_dns(target):
    try:
        target.ip_addresses = [str(r) for r in dns.resolver.resolve(target.root_domain, 'A')]
    except:
        pass
    for typ in ('MX', 'NS', 'TXT'):
        try:
            target.dns_records[typ] = [str(r) for r in dns.resolver.resolve(target.root_domain, typ)]
        except:
            pass

async def brute_subdomains(target):
    base = target.root_domain
    sem = asyncio.Semaphore(Config.THREADS)

    async def check(sub):
        async with sem:
            fqdn = f"{sub}.{base}"
            try:
                await asyncio.get_running_loop().getaddrinfo(fqdn, 80)
                target.subdomains.add(fqdn)
                try:
                    ips = await asyncio.get_running_loop().getaddrinfo(
                        fqdn, 0, proto=socket.IPPROTO_TCP
                    )
                    target.ip_addresses.extend(
                        [ip[4][0] for ip in ips if ip[4][0] not in target.ip_addresses]
                    )
                except:
                    pass
                logger_scout.info(f"Found subdomain: {fqdn}")
            except:
                pass

    tasks = [check(s) for s in Config.SUBDOMAIN_WORDLIST]
    await asyncio.gather(*tasks)

async def crt_sh_lookup(target):
    url = f"https://crt.sh/?q=%.{target.root_domain}&output=json"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for entry in data:
                        name = entry.get('name_value', '')
                        if name and name.endswith(target.root_domain):
                            target.subdomains.add(name.replace('*.', ''))
        except:
            pass

COMMON_PORTS = {
    21: 'ftp', 22: 'ssh', 23: 'telnet', 25: 'smtp', 53: 'dns',
    80: 'http', 110: 'pop3', 111: 'rpcbind', 135: 'msrpc', 139: 'netbios',
    143: 'imap', 443: 'https', 445: 'smb', 993: 'imaps', 995: 'pop3s',
    1723: 'pptp', 3306: 'mysql', 3389: 'rdp', 5432: 'postgresql',
    5900: 'vnc', 6379: 'redis', 8080: 'http-proxy', 8443: 'https-alt',
    9200: 'elasticsearch', 27017: 'mongodb'
}

async def scan_port(ip, port, timeout=2):
    try:
        loop = asyncio.get_running_loop()
        conn = await asyncio.wait_for(
            loop.sock_connect(socket.socket(socket.AF_INET, socket.SOCK_STREAM), (ip, port)),
            timeout
        )
        conn.close()
        return port
    except:
        return None

async def port_scan(target):
    if not target.ip_addresses:
        try:
            ips = await asyncio.get_running_loop().getaddrinfo(target.root_domain, 0)
            target.ip_addresses = list(set([ip[4][0] for ip in ips]))
        except:
            logger_scout.error("No IPs")
            return

    sem = asyncio.Semaphore(Config.THREADS * 2)

    async def check_one(ip, port):
        async with sem:
            res = await scan_port(ip, port)
            if res:
                target.open_ports[f"{ip}:{res}"] = COMMON_PORTS.get(res, f"unknown-{res}")
                logger_scout.info(f"Open port {res} on {ip}")

    tasks = [
        check_one(ip, port)
        for ip in target.ip_addresses
        for port in COMMON_PORTS
    ]
    await asyncio.gather(*tasks)

async def fingerprint_web(target):
    url = target.base_url
    async with aiohttp.ClientSession() as session:
        resp, body = await fetch_url(session, url)
        if resp:
            headers = resp.headers
            target.web_technologies['server'] = headers.get('Server', '')
            target.web_technologies['x-powered-by'] = headers.get('X-Powered-By', '')
            target.web_technologies['content-type'] = headers.get('Content-Type', '')
            target.cookies = {k: v.value for k, v in resp.cookies.items()}
            if headers.get('Content-Security-Policy'):
                target.csp_headers['csp'] = headers['Content-Security-Policy']
            if headers.get('Strict-Transport-Security'):
                target.csp_headers['hsts'] = headers['Strict-Transport-Security']

            soup = BeautifulSoup(body, 'lxml')
            gen = soup.find('meta', attrs={'name': 'generator'})
            if gen and gen.get('content'):
                target.web_technologies['generator'] = gen['content']

            for script in soup.find_all('script'):
                src = script.get('src', '')
                if 'jquery' in src.lower():
                    target.web_technologies['jquery'] = 'detected'
                if 'bootstrap' in src.lower():
                    target.web_technologies['bootstrap'] = 'detected'
                if 'angular' in src.lower():
                    target.web_technologies['angular'] = 'detected'
                if 'react' in src.lower():
                    target.web_technologies['react'] = 'detected'

            if '/wp-content/' in str(body) or 'wp-json' in str(body):
                target.web_technologies['cms'] = 'WordPress'

async def dir_brute(target):
    base = target.base_url
    sem = asyncio.Semaphore(Config.THREADS)

    async with aiohttp.ClientSession() as session:
        async def check(path):
            url = urljoin(base, path)
            async with sem:
                resp, _ = await fetch_url(session, url, timeout=5)
                if resp and resp.status in (200, 301, 302, 403, 401):
                    target.directories_found.append({'path': path, 'status': resp.status})
                    logger_scout.info(f"Found {path} -> {resp.status}")

        tasks = [check(p) for p in Config.DIR_WORDLIST]
        await asyncio.gather(*tasks)

async def harvest_emails(target):
    url = target.base_url
    async with aiohttp.ClientSession() as session:
        resp, body = await fetch_url(session, url)
        if resp:
            text = body.decode('utf-8', errors='ignore')
            target.emails.update(re.findall(EMAIL_RE, text))

        for path in ['/robots.txt', '/sitemap.xml']:
            resp2, body2 = await fetch_url(session, urljoin(url, path))
            if resp2 and resp2.status == 200:
                text2 = body2.decode('utf-8', errors='ignore')
                target.emails.update(re.findall(EMAIL_RE, text2))

SOCIAL_PLATFORMS = {
    'twitter': 'https://twitter.com/{username}',
    'facebook': 'https://facebook.com/{username}',
    'instagram': 'https://instagram.com/{username}',
    'linkedin': 'https://linkedin.com/in/{username}',
    'github': 'https://github.com/{username}',
    'youtube': 'https://youtube.com/@{username}',
    'reddit': 'https://reddit.com/user/{username}',
    'tiktok': 'https://tiktok.com/@{username}',
    'pinterest': 'https://pinterest.com/{username}',
    'tumblr': 'https://{username}.tumblr.com',
    'snapchat': 'https://snapchat.com/add/{username}',
    'telegram': 'https://t.me/{username}',
    'whatsapp': 'https://wa.me/{username}',
    'discord': 'https://discord.com/users/{username}',
    'twitch': 'https://twitch.tv/{username}',
    'medium': 'https://medium.com/@{username}',
    'quora': 'https://quora.com/profile/{username}',
    'patreon': 'https://patreon.com/{username}',
    'dev.to': 'https://dev.to/{username}',
    'keybase': 'https://keybase.io/{username}',
    'pastebin': 'https://pastebin.com/u/{username}',
    'bitbucket': 'https://bitbucket.org/{username}',
    'gitlab': 'https://gitlab.com/{username}',
    'hackernews': 'https://news.ycombinator.com/user?id={username}',
    'producthunt': 'https://producthunt.com/@{username}',
    'angellist': 'https://angel.co/u/{username}',
    'fiverr': 'https://fiverr.com/{username}',
    'upwork': 'https://upwork.com/freelancers/{username}',
    'behance': 'https://behance.net/{username}',
    'dribbble': 'https://dribbble.com/{username}',
    'stackoverflow': 'https://stackoverflow.com/users/{username}',
}

async def search_social(target, username):
    async with aiohttp.ClientSession() as session:
        for platform, url_template in SOCIAL_PLATFORMS.items():
            url = url_template.format(username=username)
            try:
                async with session.head(url, timeout=5, allow_redirects=True) as resp:
                    if resp.status == 200:
                        target.social_handles[platform] = url
                        logger_scout.info(f"Found {platform} profile: {url}")
            except:
                pass

async def wayback_scrape(target):
    url = f"https://web.archive.org/cdx/search/cdx?url={target.root_domain}/*&output=json&fl=original&collapse=urlkey"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=15) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    target.wayback_urls = [row[0] for row in data[1:]]
        except:
            pass

async def google_dorks(target):
    target.dork_results = [
        f"site:{target.root_domain} filetype:pdf",
        f"site:{target.root_domain} filetype:xls",
        f"site:{target.root_domain} inurl:login",
        f"site:{target.root_domain} inurl:admin",
        f"site:{target.root_domain} intitle:index of /",
        f"site:{target.root_domain} ext:env",
        f"site:{target.root_domain} ext:sql",
        f"site:{target.root_domain} 'password'",
        f"site:{target.root_domain} 'api_key'",
        f"site:{target.root_domain} 'secret'",
    ]

async def github_scan(target):
    if not Config.GITHUB_TOKEN:
        return
    headers = {'Authorization': f'token {Config.GITHUB_TOKEN}'}
    query = f'"{target.root_domain}" OR "{target.parsed.netloc}"'
    url = f"https://api.github.com/search/code?q={quote(query)}+extension:env+extension:json+extension:config+extension:yml+extension:yaml"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, timeout=15) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    target.github_secrets = [item['html_url'] for item in data.get('items', [])]
        except:
            pass

async def analyze_ssl(target):
    host = target.root_domain
    ctx = ssl.create_default_context()
    try:
        with socket.create_connection((host, 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
                target.ssl_cert = {
                    'subject': dict(cert['subject'][0]),
                    'issuer': dict(cert['issuer'][0]),
                    'notBefore': cert['notBefore'],
                    'notAfter': cert['notAfter'],
                    'serial': cert['serialNumber'],
                }
    except:
        pass

async def shodan_lookup(target):
    if not Config.SHODAN_API_KEY:
        return
    import shodan
    try:
        api = shodan.Shodan(Config.SHODAN_API_KEY)
        info = api.host(target.ip_addresses[0]) if target.ip_addresses else None
        if info:
            target.shodan_info = info
    except:
        pass

async def virustotal_lookup(target):
    if not Config.VIRUSTOTAL_API_KEY:
        return
    url = f"https://www.virustotal.com/api/v3/domains/{target.root_domain}"
    headers = {'x-apikey': Config.VIRUSTOTAL_API_KEY}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, timeout=10) as resp:
                if resp.status == 200:
                    target.virustotal_info = await resp.json()
        except:
            pass

async def check_vulnerabilities(target):
    vulns = []
    for port_str, service in target.open_ports.items():
        if service in ['ftp', 'telnet', 'rdp', 'vnc'] and 'secure' not in service:
            vulns.append(f"Insecure service '{service}' on {port_str}")
    if target.ssl_cert:
        try:
            not_after = datetime.strptime(target.ssl_cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            if not_after < datetime.utcnow():
                vulns.append("SSL certificate expired")
        except:
            pass
    target.vulnerabilities = vulns

class OmegaScout:
    def __init__(self, domain):
        self.target = Target(domain)
        self.start_time = datetime.utcnow()

    async def run(self, progress_callback=None):
        if progress_callback:
            progress_callback("Starting OmegaScout")

        await asyncio.gather(
            resolve_dns(self.target),
            brute_subdomains(self.target),
            crt_sh_lookup(self.target),
            port_scan(self.target),
            fingerprint_web(self.target),
            dir_brute(self.target),
            harvest_emails(self.target),
            wayback_scrape(self.target),
            google_dorks(self.target),
            github_scan(self.target),
            analyze_ssl(self.target),
            shodan_lookup(self.target),
            virustotal_lookup(self.target),
            check_vulnerabilities(self.target),
        )

        for email in self.target.emails:
            local = email.split('@')[0]
            if local:
                await search_social(self.target, local)

        if progress_callback:
            progress_callback("OmegaScout completed")
        return self.target

    def generate_reports(self):
        os.makedirs(Config.OUTPUT_DIR, exist_ok=True)

        data = {
            'target': self.target.root_domain,
            'timestamp': self.start_time.isoformat(),
            'ip_addresses': self.target.ip_addresses,
            'subdomains': list(self.target.subdomains),
            'open_ports': self.target.open_ports,
            'web_technologies': self.target.web_technologies,
            'emails': list(self.target.emails),
            'social_handles': self.target.social_handles,
            'dns_records': self.target.dns_records,
            'ssl_cert': self.target.ssl_cert,
            'wayback_urls': self.target.wayback_urls[:50],
            'github_secrets': self.target.github_secrets,
            'vulnerabilities': self.target.vulnerabilities,
            'directories_found': self.target.directories_found,
            'shodan_info': self.target.shodan_info,
            'virustotal_info': self.target.virustotal_info,
        }

        with open(Config.JSON_REPORT, 'w') as f:
            json.dump(data, f, indent=2, default=str)

        with open(Config.CSV_REPORT, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['Domain', 'Subdomain', 'IP', 'Port', 'Service', 'Email', 'Social', 'Vuln'])
            for sub in self.target.subdomains:
                w.writerow([self.target.root_domain, sub, '', '', '', '', '', ''])
            for ip in self.target.ip_addresses:
                w.writerow([self.target.root_domain, '', ip, '', '', '', '', ''])
            for port, svc in self.target.open_ports.items():
                w.writerow([self.target.root_domain, '', '', port, svc, '', '', ''])
            for email in self.target.emails:
                w.writerow([self.target.root_domain, '', '', '', '', email, '', ''])
            for platform, url in self.target.social_handles.items():
                w.writerow([self.target.root_domain, '', '', '', '', '', f"{platform}:{url}", ''])
            for vuln in self.target.vulnerabilities:
                w.writerow([self.target.root_domain, '', '', '', '', '', '', vuln])

        html = f"""<html><head><title>OmegaScout Report for {self.target.root_domain}</title></head><body>
        <h1>OmegaScout - {self.target.root_domain}</h1>
        <p>Generated: {datetime.utcnow().isoformat()}</p>
        <h2>Subdomains</h2><ul>{"".join(f"<li>{s}</li>" for s in self.target.subdomains)}</ul>
        <h2>Open Ports</h2><ul>{"".join(f"<li>{p} : {s}</li>" for p,s in self.target.open_ports.items())}</ul>
        <h2>Emails</h2><ul>{"".join(f"<li>{e}</li>" for e in self.target.emails)}</ul>
        <h2>Social Handles</h2><ul>{"".join(f"<li>{p}: <a href='{u}'>{u}</a></li>" for p,u in self.target.social_handles.items())}</ul>
        <h2>Vulnerabilities</h2><ul>{"".join(f"<li style='color:red'>{v}</li>" for v in self.target.vulnerabilities)}</ul>
        <h2>Web Tech</h2><pre>{json.dumps(self.target.web_technologies, indent=2)}</pre>
        </body></html>
        """
        with open(Config.HTML_REPORT, 'w') as f:
            f.write(html)

# ══════════════════════════════════════════════════════════════════════
#  NUMBERBOOK
# ══════════════════════════════════════════════════════════════════════
class NumberbookScanner:
    def __init__(self):
        load_dotenv()
        self.api_id = os.getenv("TELEGRAM_API_ID")
        self.api_hash = os.getenv("TELEGRAM_API_HASH")
        self.bot_username = os.getenv("BOT_USERNAME")
        if not all([self.api_id, self.api_hash, self.bot_username]):
            raise ValueError("Missing TELEGRAM_API_ID, TELEGRAM_API_HASH or BOT_USERNAME in .env")
        self.client = TelegramClient('session_name', int(self.api_id), self.api_hash)

    async def fetch_number_data(self, phone_number):
        try:
            await self.client.start()
            async with self.client.conversation(self.bot_username, timeout=15) as conv:
                await conv.send_message(phone_number)
                response = await conv.get_response()
                return response.text
        except TimeoutError:
            return "Error: Bot response timeout."
        except Exception as e:
            return f"Error: {str(e)}"
        finally:
            await self.client.disconnect()

# ══════════════════════════════════════════════════════════════════════
#  PYSIDE6 GUI WORKERS
# ══════════════════════════════════════════════════════════════════════
class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(str)
    result = Signal(object)
    progress = Signal(int, int)
    log = Signal(str)
    status = Signal(str)

class Worker(QThread):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.signals.result.emit(result)
        except Exception as e:
            self.signals.error.emit(str(e))
        finally:
            self.signals.finished.emit()

# ── HR TAB ──────────────────────────────────────────────────────────────
class HREmailHunterTab(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        g = QGroupBox("Target & Options")
        f = QFormLayout(g)

        self.domain_edit = QLineEdit()
        self.domain_edit.setPlaceholderText("example.com")
        f.addRow("Domain:", self.domain_edit)

        self.hunter_key_edit = QLineEdit()
        self.hunter_key_edit.setPlaceholderText("Hunter.io API key (optional)")
        f.addRow("Hunter API Key:", self.hunter_key_edit)

        self.names_edit = QLineEdit()
        self.names_edit.setPlaceholderText("Jane Doe, John Smith")
        f.addRow("Recruiter Names:", self.names_edit)

        self.instagram_edit = QLineEdit()
        self.instagram_edit.setPlaceholderText("Instagram handle (optional)")
        f.addRow("Instagram:", self.instagram_edit)

        self.tiktok_edit = QLineEdit()
        self.tiktok_edit.setPlaceholderText("TikTok handle (optional)")
        f.addRow("TikTok:", self.tiktok_edit)

        self.export_cb = QCheckBox("Export CSV + JSON")
        self.export_cb.setChecked(True)
        self.report_cb = QCheckBox("Generate HTML report")
        self.report_cb.setChecked(True)
        hl = QHBoxLayout()
        hl.addWidget(self.export_cb)
        hl.addWidget(self.report_cb)
        f.addRow("Options:", hl)

        self.workers_spin = QSpinBox()
        self.workers_spin.setRange(1, 30)
        self.workers_spin.setValue(15)
        f.addRow("Threads:", self.workers_spin)

        layout.addWidget(g)

        bl = QHBoxLayout()
        self.start_btn = QPushButton("▶ Start Scan")
        self.start_btn.clicked.connect(self.start_scan)
        self.stop_btn = QPushButton("■ Stop")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_scan)
        self.clear_btn = QPushButton("Clear Log")
        self.clear_btn.clicked.connect(self.clear_log)
        bl.addWidget(self.start_btn)
        bl.addWidget(self.stop_btn)
        bl.addWidget(self.clear_btn)
        bl.addStretch()
        layout.addLayout(bl)

        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFont(QFont("Consolas", 9))
        layout.addWidget(self.log_output)

        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

    def log(self, msg):
        self.log_output.append(msg)
        self.log_output.verticalScrollBar().setValue(
            self.log_output.verticalScrollBar().maximum()
        )

    def clear_log(self):
        self.log_output.clear()

    def start_scan(self):
        domain = self.domain_edit.text().strip()
        if not domain:
            QMessageBox.warning(self, "Missing domain", "Please enter a domain.")
            return

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress.setVisible(True)
        self.log("Starting HR scan...")

        class Args:
            pass
        args = Args()
        args.domain = domain
        args.hunter_key = self.hunter_key_edit.text().strip() or None
        names = [n.strip() for n in self.names_edit.text().split(",") if n.strip()]
        args.names = names if names else None
        args.instagram = self.instagram_edit.text().strip() or None
        args.tiktok = self.tiktok_edit.text().strip() or None
        args.workers = self.workers_spin.value()
        args.export = self.export_cb.isChecked()
        args.report = self.report_cb.isChecked()
        args.abstract_key = None

        def worker_fn():
            return hr_run(args, log_cb=self.log)

        self.worker = Worker(worker_fn)
        self.worker.signals.result.connect(self.on_scan_finished)
        self.worker.signals.error.connect(self.on_scan_error)
        self.worker.signals.finished.connect(self.on_scan_done)
        self.worker.start()

    def on_scan_finished(self, result):
        self.log("Scan completed.")

    def on_scan_error(self, error):
        self.log(f"Error: {error}")

    def on_scan_done(self):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress.setVisible(False)

    def stop_scan(self):
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.log("Scan stopped.")

# ── INSTAGRAM TAB ──────────────────────────────────────────────────────
class InstagramTab(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()
        self.last_sessionid = ""
        self.last_csrftoken = ""
        self.last_user_id = ""
        self.last_target = ""

    def init_ui(self):
        layout = QVBoxLayout(self)
        g = QGroupBox("Instagram Credentials")
        f = QFormLayout(g)

        self.sessionid_edit = QLineEdit()
        self.sessionid_edit.setPlaceholderText("sessionid cookie")
        f.addRow("Session ID:", self.sessionid_edit)

        self.csrftoken_edit = QLineEdit()
        self.csrftoken_edit.setPlaceholderText("csrftoken cookie")
        f.addRow("CSRF Token:", self.csrftoken_edit)

        self.userid_edit = QLineEdit()
        self.userid_edit.setPlaceholderText("ds_user_id")
        f.addRow("User ID:", self.userid_edit)

        self.target_edit = QLineEdit()
        self.target_edit.setPlaceholderText("username (optional)")
        f.addRow("Target Username:", self.target_edit)

        self.load_json_btn = QPushButton("📂 Load Cookies JSON")
        self.load_json_btn.clicked.connect(self.load_json)
        f.addRow(self.load_json_btn)

        layout.addWidget(g)

        bl = QHBoxLayout()
        self.fetch_btn = QPushButton("🚀 Fetch Profile")
        self.fetch_btn.clicked.connect(self.fetch_profile)
        self.clear_btn = QPushButton("Clear Output")
        self.clear_btn.clicked.connect(self.clear_output)
        self.retry_btn = QPushButton("🔁 Retry")
        self.retry_btn.setEnabled(False)
        self.retry_btn.clicked.connect(self.retry_fetch)
        bl.addWidget(self.fetch_btn)
        bl.addWidget(self.retry_btn)
        bl.addWidget(self.clear_btn)
        bl.addStretch()
        layout.addLayout(bl)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Consolas", 9))
        layout.addWidget(self.output)

        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

    def log(self, msg):
        self.output.append(msg)
        self.output.verticalScrollBar().setValue(
            self.output.verticalScrollBar().maximum()
        )

    def clear_output(self):
        self.output.clear()

    def load_json(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Cookies JSON", "", "JSON Files (*.json)"
        )
        if not path:
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if 'sessionid' in data:
                self.sessionid_edit.setText(data['sessionid'])
            if 'csrftoken' in data:
                self.csrftoken_edit.setText(data['csrftoken'])
            if 'ds_user_id' in data:
                self.userid_edit.setText(str(data['ds_user_id']))
            if 'target' in data:
                self.target_edit.setText(data['target'])
            self.log(f"✅ Loaded cookies from {path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load JSON:\n{e}")

    def fetch_profile(self):
        sid = self.sessionid_edit.text().strip()
        csrf = self.csrftoken_edit.text().strip()
        uid = self.userid_edit.text().strip()
        target = self.target_edit.text().strip() or None
        if not sid or not csrf or not uid:
            QMessageBox.warning(
                self,
                "Missing Fields",
                "Please fill in Session ID, CSRF Token, and User ID."
            )
            return
        self.last_sessionid = sid
        self.last_csrftoken = csrf
        self.last_user_id = uid
        self.last_target = target
        self.start_fetch(sid, csrf, uid, target)

    def retry_fetch(self):
        if not self.last_sessionid:
            return
        self.start_fetch(
            self.last_sessionid,
            self.last_csrftoken,
            self.last_user_id,
            self.last_target
        )

    def start_fetch(self, sid, csrf, uid, target):
        self.fetch_btn.setEnabled(False)
        self.retry_btn.setEnabled(False)
        self.output.clear()
        self.log("⏳ Fetching profile...")

        def worker_fn():
            return fetch_profile(sid, csrf, uid, target, status_callback=self.log)

        self.worker = Worker(worker_fn)
        self.worker.signals.result.connect(self.on_fetch_result)
        self.worker.signals.error.connect(self.on_fetch_error)
        self.worker.signals.finished.connect(self.on_fetch_done)
        self.worker.start()

    def on_fetch_result(self, result):
        if 'error' in result:
            self.log(f"❌ ERROR: {result['error']}")
        elif result.get('success') and 'profile' in result:
            self.log(print_profile_text(result['profile']))
            self.log("\n✅ Profile fetched successfully.")
        else:
            self.log("❌ Unexpected result.")

    def on_fetch_error(self, error):
        self.log(f"Error: {error}")

    def on_fetch_done(self):
        self.fetch_btn.setEnabled(True)
        self.retry_btn.setEnabled(True)

# ── OSINT TAB ──────────────────────────────────────────────────────────
class OSINTTab(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        tl = QHBoxLayout()
        self.domain_edit = QLineEdit()
        self.domain_edit.setPlaceholderText("example.com")
        tl.addWidget(QLabel("Domain:"))
        tl.addWidget(self.domain_edit)
        self.scan_btn = QPushButton("▶ Scan")
        self.scan_btn.clicked.connect(self.start_scan)
        self.stop_btn = QPushButton("■ Stop")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_scan)
        tl.addWidget(self.scan_btn)
        tl.addWidget(self.stop_btn)
        layout.addLayout(tl)

        mg = QGroupBox("Modules")
        gl = QGridLayout(mg)
        self.module_vars = {}
        for i, (name, _) in enumerate(MODULES):
            var = QCheckBox(name)
            var.setChecked(True)
            self.module_vars[name] = var
            gl.addWidget(var, i // 3, i % 3)
        layout.addWidget(mg)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Consolas", 9))
        layout.addWidget(self.output)

        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

    def log(self, msg):
        self.output.append(msg)
        self.output.verticalScrollBar().setValue(
            self.output.verticalScrollBar().maximum()
        )

    def start_scan(self):
        domain = self.domain_edit.text().strip()
        if not domain:
            QMessageBox.warning(self, "Missing domain", "Please enter a domain.")
            return

        selected = [name for name, var in self.module_vars.items() if var.isChecked()]
        if not selected:
            QMessageBox.warning(self, "No modules", "Select at least one module.")
            return

        self.scan_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.output.clear()
        self.log(f"Scanning {domain} with modules: {', '.join(selected)}")

        def worker_fn():
            results = {}
            for name in selected:
                fn = MODULE_MAP[name]
                try:
                    self.log(f"Running {name}...")
                    results[name] = fn(domain)
                except Exception as e:
                    self.log(f"Error in {name}: {e}")
                    results[name] = {"error": str(e)}
            return results

        self.worker = Worker(worker_fn)
        self.worker.signals.result.connect(self.on_scan_result)
        self.worker.signals.error.connect(self.on_scan_error)
        self.worker.signals.finished.connect(self.on_scan_done)
        self.worker.start()

    def on_scan_result(self, results):
        self.log("\n=== Scan Results ===")
        for name, data in results.items():
            self.log(f"{name}: {data}")
        path = save_results(self.domain_edit.text().strip(), results)
        self.log(f"\nResults saved to {path}")

    def on_scan_error(self, error):
        self.log(f"Error: {error}")

    def on_scan_done(self):
        self.scan_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

    def stop_scan(self):
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.log("Scan stopped.")

# ── TIKTOK TAB ─────────────────────────────────────────────────────────
class TikTokTab(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        il = QHBoxLayout()
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("username")
        self.fetch_btn = QPushButton("🔍 Fetch Profile")
        self.fetch_btn.clicked.connect(self.fetch_profile)
        il.addWidget(QLabel("Username:"))
        il.addWidget(self.username_edit)
        il.addWidget(self.fetch_btn)
        il.addStretch()
        layout.addLayout(il)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Consolas", 9))
        layout.addWidget(self.output)

        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

    def log(self, msg):
        self.output.append(msg)
        self.output.verticalScrollBar().setValue(
            self.output.verticalScrollBar().maximum()
        )

    def fetch_profile(self):
        username = self.username_edit.text().strip()
        if not username:
            QMessageBox.warning(
                self,
                "Missing username",
                "Please enter a TikTok username."
            )
            return

        self.fetch_btn.setEnabled(False)
        self.output.clear()
        self.log(f"Fetching TikTok profile for @{username}...")

        def worker_fn():
            return get_profile_data(username)

        self.worker = Worker(worker_fn)
        self.worker.signals.result.connect(self.on_result)
        self.worker.signals.error.connect(self.on_error)
        self.worker.signals.finished.connect(self.on_done)
        self.worker.start()

    def on_result(self, data):
        if "error" in data:
            self.log(f"❌ Error: {data['error']}")
        else:
            self.log("=== TikTok Profile ===")
            self.log(f"User ID: {data.get('user_id')}")
            self.log(f"Username: @{data.get('unique_id')}")
            self.log(f"Nickname: {fix_rtl(data.get('nickname', ''))}")
            self.log(f"Bio: {fix_rtl(data.get('bio', ''))}")
            self.log(f"Followers: {data.get('follower_count', 0):,}")
            self.log(f"Following: {data.get('following_count', 0):,}")
            self.log(f"Likes: {data.get('heart_count', 0):,}")
            self.log(f"Videos: {data.get('video_count', 0):,}")
            self.log(f"Verified: {data.get('is_verified')}")
            self.log(f"Private: {data.get('is_private')}")
            self.log(f"Region: {data.get('region')}")
            if data.get('created'):
                dt = datetime.fromtimestamp(data['created'])
                self.log(f"Joined: {dt.strftime('%Y-%m-%d %H:%M')}")
            self.log("✅ Done.")

    def on_error(self, error):
        self.log(f"Error: {error}")

    def on_done(self):
        self.fetch_btn.setEnabled(True)

# ── OMEGASCOUT TAB ─────────────────────────────────────────────────────
class OmegaScoutTab(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        g = QGroupBox("Target")
        f = QFormLayout(g)
        self.domain_edit = QLineEdit()
        self.domain_edit.setPlaceholderText("example.com")
        f.addRow("Domain:", self.domain_edit)
        layout.addWidget(g)

        bl = QHBoxLayout()
        self.start_btn = QPushButton("▶ Start OmegaScout")
        self.start_btn.clicked.connect(self.start_scan)
        self.stop_btn = QPushButton("■ Stop")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_scan)
        self.clear_btn = QPushButton("Clear Log")
        self.clear_btn.clicked.connect(self.clear_log)
        bl.addWidget(self.start_btn)
        bl.addWidget(self.stop_btn)
        bl.addWidget(self.clear_btn)
        bl.addStretch()
        layout.addLayout(bl)

        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFont(QFont("Consolas", 9))
        layout.addWidget(self.log_output)

        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

    def log(self, msg):
        self.log_output.append(msg)
        self.log_output.verticalScrollBar().setValue(
            self.log_output.verticalScrollBar().maximum()
        )

    def clear_log(self):
        self.log_output.clear()

    def start_scan(self):
        domain = self.domain_edit.text().strip()
        if not domain:
            QMessageBox.warning(self, "Missing domain", "Enter a domain.")
            return

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress.setVisible(True)
        self.log(f"Starting OmegaScout on {domain}")

        def worker_fn():
            scout = OmegaScout(domain)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                target = loop.run_until_complete(scout.run())
                scout.generate_reports()
                return target
            finally:
                loop.close()

        self.worker = Worker(worker_fn)
        self.worker.signals.result.connect(self.on_result)
        self.worker.signals.error.connect(self.on_error)
        self.worker.signals.finished.connect(self.on_done)
        self.worker.start()

    def on_result(self, target):
        self.log("=== OmegaScout Results ===")
        self.log(f"IPs: {target.ip_addresses}")
        self.log(f"Subdomains: {len(target.subdomains)} found")
        self.log(f"Open ports: {target.open_ports}")
        self.log(f"Emails: {target.emails}")
        self.log(f"Vulnerabilities: {target.vulnerabilities}")
        self.log(f"Reports saved in {Config.OUTPUT_DIR}")

    def on_error(self, error):
        self.log(f"Error: {error}")

    def on_done(self):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress.setVisible(False)

    def stop_scan(self):
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.log("Scan stopped.")

# ── NUMBERBOOK TAB ─────────────────────────────────────────────────────
class NumberbookTab(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        g = QGroupBox("Phone Number")
        f = QFormLayout(g)
        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("+1234567890")
        f.addRow("Number:", self.phone_edit)
        layout.addWidget(g)

        bl = QHBoxLayout()
        self.start_btn = QPushButton("🔍 Lookup")
        self.start_btn.clicked.connect(self.lookup)
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_output)
        bl.addWidget(self.start_btn)
        bl.addWidget(self.clear_btn)
        bl.addStretch()
        layout.addLayout(bl)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Consolas", 9))
        layout.addWidget(self.output)

        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

    def log(self, msg):
        self.output.append(msg)
        self.output.verticalScrollBar().setValue(
            self.output.verticalScrollBar().maximum()
        )

    def clear_output(self):
        self.output.clear()

    def lookup(self):
        phone = self.phone_edit.text().strip()
        if not phone:
            QMessageBox.warning(self, "Missing number", "Enter a phone number.")
            return

        self.start_btn.setEnabled(False)
        self.output.clear()
        self.log(f"Looking up {phone} via Telegram bot...")

        def worker_fn():
            scanner = NumberbookScanner()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(scanner.fetch_number_data(phone))
                return result
            finally:
                loop.close()

        self.worker = Worker(worker_fn)
        self.worker.signals.result.connect(self.on_result)
        self.worker.signals.error.connect(self.on_error)
        self.worker.signals.finished.connect(self.on_done)
        self.worker.start()

    def on_result(self, data):
        self.log("=== Result ===")
        self.log(data)

    def on_error(self, error):
        self.log(f"Error: {error}")

    def on_done(self):
        self.start_btn.setEnabled(True)

# ══════════════════════════════════════════════════════════════════════
#  MAIN WINDOW
# ══════════════════════════════════════════════════════════════════════
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(
            f"ΩMEGASCOUT · UNIFIED OSINT v{VERSION}  —  dev by naif‑khaled  🇸🇦"
        )
        self.setGeometry(50, 50, 1400, 950)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)

        banner_text = (
            "☠  ΩMEGASCOUT  ☠\n"
            "  UNIFIED OSINT SUITE\n"
            "  dev by naif‑khaled\n"
            "  ███╗   ███╗ █████╗ ██████╗ ███████╗    ██╗███╗   ██╗\n"
            "  ████╗ ████║██╔══██╗██╔══██╗██╔════╝    ██║████╗  ██║\n"
            "  ██╔████╔██║███████║██║  ██║█████╗      ██║██╔██╗ ██║\n"
            "  ██║╚██╔╝██║██╔══██║██║  ██║██╔══╝      ██║██║╚██╗██║\n"
            "  ██║ ╚═╝ ██║██║  ██║██████╔╝███████╗    ██║██║ ╚████║\n"
            "  ╚═╝     ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝    ╚═╝╚═╝  ╚═══╝\n"
            "  MADE IN SAUDI  🇸🇦"
        )

        logo = QLabel(banner_text)
        logo.setObjectName("logo_label")
        logo.setAlignment(Qt.AlignCenter)
        logo.setFont(QFont("Consolas", 18, QFont.Bold))
        logo.setStyleSheet(
            """
            QLabel#logo_label {
                font-size: 22px;
                font-weight: bold;
                color: #d32f2f;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #0a0a0f, stop:0.3 #1a1010,
                                            stop:0.7 #1a1010, stop:1 #0a0a0f);
                border-bottom: 3px solid #d32f2f;
                padding: 15px;
                margin: 0;
            }
            """
        )
        main_layout.addWidget(logo)

        self.tabs = QTabWidget()
        self.tabs.addTab(HREmailHunterTab(), "HR Hunter")
        self.tabs.addTab(InstagramTab(), "Instagram")
        self.tabs.addTab(OSINTTab(), "OSINT Pro")
        self.tabs.addTab(TikTokTab(), "TikTok")
        self.tabs.addTab(OmegaScoutTab(), "OmegaScout")
        self.tabs.addTab(NumberbookTab(), "Numberbook")
        main_layout.addWidget(self.tabs)

        self.statusBar().showMessage(
            "🔥 Ready — dev by naif‑khaled  |  MADE IN SAUDI 🇸🇦  |  Use responsibly and ethically."
        )
        self.statusBar().setStyleSheet(
            "QStatusBar { background-color: #14141e; color: #00e5ff; font-weight: bold; }"
        )

# ══════════════════════════════════════════════════════════════════════
#  CLI BANNER AND COMMANDS
# ══════════════════════════════════════════════════════════════════════
def print_cli_banner():
    print(r"""
╔══════════════════════════════════════════════════════════════════════════╗
║   ██████╗ ███╗   ███╗███████╗ ██████╗  █████╗ ███████╗ ██████╗ ██████╗ ██╗   ██╗████████╗
║  ██╔═══██╗████╗ ████║██╔════╝██╔════╝ ██╔══██╗██╔════╝██╔═══██╗██╔══██╗██║   ██║╚══██╔══╝
║  ██║   ██║██╔████╔██║█████╗  ██║  ███╗███████║███████╗██║   ██║██████╔╝██║   ██║   ██║
║  ██║   ██║██║╚██╔╝██║██╔══╝  ██║   ██║██╔══██║╚════██║██║   ██║██╔══██╗██║   ██║   ██║
║  ╚██████╔╝██║ ╚═╝ ██║███████╗╚██████╔╝██║  ██║███████║╚██████╔╝██║  ██║╚██████╔╝   ██║
║   ╚═════╝ ╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝
║                                                                                        ║
║        UNIFIED OSINT SUITE  –  v2.0  –  dev by naif‑khaled                           ║
║   MADE IN SAUDI  🇸🇦                                                              ║
╚══════════════════════════════════════════════════════════════════════════╝
""")

def cli_omegascout(args):
    print_cli_banner()
    domain = args.domain
    print(f"\n[+] Running OmegaScout on {domain}...")
    scout = OmegaScout(domain)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(scout.run())
        scout.generate_reports()
        print(f"[+] Reports saved in {Config.OUTPUT_DIR}")
    finally:
        loop.close()

def cli_numberbook(args):
    print_cli_banner()
    phone = args.phone
    print(f"\n[+] Looking up {phone} via Telegram bot...")
    scanner = NumberbookScanner()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(scanner.fetch_number_data(phone))
        print(result)
    finally:
        loop.close()

def cli_hr(args):
    print_cli_banner()
    print("HR Email Hunter CLI – use GUI for full functionality.")

def cli_insta(args):
    print_cli_banner()
    print("Instagram Viewer CLI – use GUI for full functionality.")

def cli_osint(args):
    print_cli_banner()
    print("OSINT Pro CLI – use GUI for full functionality.")

def cli_tiktok(args):
    print_cli_banner()
    print("TikTok Recon CLI – use GUI for full functionality.")

# ══════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(description="Unified OSINT Suite – CLI mode")
    sub = parser.add_subparsers(dest="tool", required=False)

    p = sub.add_parser("hr", help="HR Email Hunter")
    p.add_argument("-d", "--domain", required=True)
    p.add_argument("-k", "--hunter-key")
    p.add_argument("-n", "--names", nargs="+")
    p.add_argument("--instagram")
    p.add_argument("--tiktok")
    p.add_argument("-w", "--workers", type=int, default=15)
    p.add_argument("--export", action="store_true")
    p.add_argument("--report", action="store_true")

    p = sub.add_parser("insta", help="Instagram Viewer")
    p.add_argument("--sessionid", required=True)
    p.add_argument("--csrftoken", required=True)
    p.add_argument("--userid", required=True)
    p.add_argument("--target")

    p = sub.add_parser("osint", help="OSINT Pro")
    p.add_argument("--cli", required=True, help="Target domain")
    p.add_argument("--modules", nargs="+", help="Modules to run")

    p = sub.add_parser("tiktok", help="TikTok Recon")
    p.add_argument("--username", required=True)

    p = sub.add_parser("scout", help="OmegaScout")
    p.add_argument("--domain", required=True)

    p = sub.add_parser("numberbook", help="Numberbook Telegram lookup")
    p.add_argument("--phone", required=True)

    args = parser.parse_args()

    if args.tool == "hr":
        cli_hr(args)
    elif args.tool == "insta":
        cli_insta(args)
    elif args.tool == "osint":
        cli_osint(args)
    elif args.tool == "tiktok":
        cli_tiktok(args)
    elif args.tool == "scout":
        cli_omegascout(args)
    elif args.tool == "numberbook":
        cli_numberbook(args)
    else:
        app = QApplication(sys.argv)
        app.setStyleSheet(DARK_STYLE)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    main()

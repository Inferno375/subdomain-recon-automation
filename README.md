# Subdomain Recon Automation Tool 🔍

A fast, multithreaded Python reconnaissance tool designed to automate subdomain discovery, perform concurrent DNS resolution, and probe live web services for page titles and HTTP status codes.

---

## 🌟 Key Features

* **Passive Reconnaissance:** Queries public Certificate Transparency (`crt.sh`) logs without directly probing the target's primary servers.
* **Data Sanitization & Deduplication:** Cleans wildcard entries (`*.`), normalizes newline characters, and uses Python `set()` structures to eliminate redundant certificates.
* **Parallel DNS Resolution:** Employs `concurrent.futures.ThreadPoolExecutor` to asynchronously resolve hostnames to IP addresses using native socket lookups.
* **HTTP/HTTPS Probing:** Automatically checks active subdomains over HTTP and HTTPS to capture HTTP response status codes and extract HTML page titles via `BeautifulSoup`.
* **Pipeline-Ready CLI:** Built with `argparse` to support standard terminal flags (`-d` for domain, `-o` for saving output) for easy integration into downstream security workflows.

---

## 🚀 Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/Inferno375/subdomain-recon-automation.git](https://github.com/Inferno375/subdomain-recon-automation.git)
   cd subdomain-recon-automation
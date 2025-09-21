#!/usr/bin/env python3
import argparse
import requests
import re
import sys
from typing import List

parser = argparse.ArgumentParser()
parser.add_argument("--url", help="PHPinfo URL: eg. https://example.com/phpinfo.php")
parser.add_argument("--file", help="PHPinfo localfile path: eg. dir/phpinfo")
parser.add_argument("-H", "--header", action="append",
                    help="Add HTTP header(s). Use either 'Name=Value' or 'Name: Value'. Can be used multiple times.",
                    default=[])
parser.add_argument("--timeout", type=int, default=10, help="Request timeout in seconds (default: 10)")
args = parser.parse_args()

class colors:
    reset = '\033[0m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'

print(colors.green + r"""

                                ,---,     
                                  .'  .' `\   
                                  ,---.'     \  
                                  |   |  .`\  | 
                                  :   : |  '  | 
                                  |   ' '  ;  : 
                                  '   | ;  .  | 
                                  |   | :  |  ' 
                                  '   : | /  ;  
                                  |   | '` ,/   
                                  ;   :  .'     
                                  |   ,.'       
                                  '---'         

""" + "\n\t\t\t" + colors.blue + "authors: " + colors.orange + "__c3rb3ru5__" + ", " + "$_SpyD3r_$" + "\n" + colors.reset)

# Build headers dict from provided -H args
def parse_headers(header_list: List[str]) -> dict:
    hdrs = {}
    for h in header_list:
        if '=' in h and ':' not in h:
            name, val = h.split('=', 1)
        elif ':' in h:
            name, val = h.split(':', 1)
        else:
            # malformed, ignore
            continue
        hdrs[name.strip()] = val.strip()
    return hdrs

HEADERS = parse_headers(args.header)

phpinfo = ""
if args.url:
    url = args.url
    try:
        resp = requests.get(url, headers=HEADERS if HEADERS else None, timeout=args.timeout)
        # fallback: try without headers if first request didn't return 200 and headers were used
        if resp.status_code != 200 and HEADERS:
            resp = requests.get(url, timeout=args.timeout)
        resp.raise_for_status()
        phpinfo = resp.text
    except requests.RequestException as e:
        print(colors.red + "[!] Error fetching URL: {}{}".format(e, colors.reset))
        sys.exit(1)

elif args.file:
    phpinfofile = args.file
    try:
        with open(phpinfofile, 'r', encoding='utf-8', errors='replace') as f:
            phpinfo = f.read()
    except OSError as e:
        print(colors.red + "[!] Error reading file: {}{}".format(e, colors.reset))
        sys.exit(1)
else:
    parser.print_help()
    sys.exit(1)

modules = []
inp = []

# Robust extraction of disable_functions from phpinfo HTML
def extract_disable_functions(phpinfo_text: str) -> List[str]:
    # Pattern 1: <td class="v">value</td> after a disable_functions label
    m = re.search(r'disable_functions.*?<td[^>]*class=["\']?v["\']?[^>]*>(.*?)</td>', phpinfo_text, re.IGNORECASE|re.DOTALL)
    if m:
        raw = re.sub(r'<[^>]*>', '', m.group(1)).strip()
        if raw:
            return [x.strip() for x in raw.split(',') if x.strip()]
    # Pattern 2: generic key/value table layout
    m2 = re.search(r'<tr>\s*<td[^>]*>\s*disable_functions\s*</td>\s*<td[^>]*>\s*(.*?)\s*</td>\s*</tr>', phpinfo_text, re.IGNORECASE|re.DOTALL)
    if m2:
        raw = re.sub(r'<[^>]*>', '', m2.group(1)).strip()
        if raw:
            return [x.strip() for x in raw.split(',') if x.strip()]
    # Pattern 3: plain text fallback (in case someone pasted text)
    m3 = re.search(r'disable_functions\s*[:=]\s*([A-Za-z0-9_,\s-]+)', phpinfo_text, re.IGNORECASE)
    if m3:
        raw = m3.group(1).strip()
        if raw:
            return [x.strip() for x in raw.split(',') if x.strip()]
    return []

inp = extract_disable_functions(phpinfo)

dangerous_functions = [
    'pcntl_alarm','pcntl_fork','pcntl_waitpid','pcntl_wait','pcntl_wifexited','pcntl_wifstopped',
    'pcntl_wifsignaled','pcntl_wifcontinued','pcntl_wexitstatus','pcntl_wtermsig','pcntl_wstopsig',
    'pcntl_signal','pcntl_signal_get_handler','pcntl_signal_dispatch','pcntl_get_last_error',
    'pcntl_strerror','pcntl_sigprocmask','pcntl_sigwaitinfo','pcntl_sigtimedwait','pcntl_exec',
    'pcntl_getpriority','pcntl_setpriority','pcntl_async_signals','error_log','system','exec',
    'shell_exec','popen','proc_open','passthru','link','symlink','syslog','ld','mail'
]

if "mbstring.ini" in phpinfo:
    modules += ['mbstring']
    dangerous_functions += ['mb_send_mail']

if "imap.ini" in phpinfo:
    modules += ['imap']
    dangerous_functions += ['imap_open','imap_mail']

if "libvirt-php.ini" in phpinfo:
    modules += ['libvert']
    dangerous_functions += ['libvirt_connect']

if "gnupg.ini" in phpinfo:
    modules += ['gnupg']
    dangerous_functions += ['gnupg_init']

if "imagick.ini" in phpinfo:
    modules += ['imagick']

exploitable_functions = []

for i in dangerous_functions:
    if i not in inp:
        exploitable_functions.append(i)

if len(exploitable_functions) == 0:
    print('\n' + colors.green + 'The disable_functions seems strong' + colors.reset)
else:
    print('\n' + colors.orange + 'Please add the following functions in your disable_functions option:' + colors.reset)
    print(','.join(exploitable_functions))

if "imagick" in modules:
    print('\n' + colors.blue + 'PHP-imagick module is present. It can be exploited using LD_PRELOAD method' + colors.reset)

if "PHP-FPM" in phpinfo:
    print(colors.orange + "If PHP-FPM is there stream_socket_sendto,stream_socket_client,fsockopen can also be used to be exploit by poisoning the request to the unix socket" + colors.reset)

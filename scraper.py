import requests
from bs4 import BeautifulSoup
import json, csv, os
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# FROZEN ZONE MAPPING
ZONES = [
    {"url": "https://www.newenglandoil.com/massachusetts/zone9.asp?x=0", "id": "MA_Zone_9", "state": "MA"},
    {"url": "https://www.newenglandoil.com/newhampshire/zone2.asp?x=0", "id": "NH_Zone_2", "state": "NH"},
    {"url": "https://www.newenglandoil.com/newhampshire/zone6.asp?x=0", "id": "NH_Zone_6", "state": "NH"}
]

def get_clean_link(a_tag):
    if not a_tag or not a_tag.get('href'): return "#"
    href = a_tag['href']
    if href.startswith('http'): return href
    if 'click.asp' in href:
        params = parse_qs(urlparse(href).query)
        if 'x' in params: return params['x'][0]
    return f"https://www.newenglandoil.com/{href.lstrip('/')}"

def scrape():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    all_vendors = []
    for z in ZONES:
        try:
            res = requests.get(z['url'], timeout=15)
            soup = BeautifulSoup(res.text, 'html.parser')
            rows = soup.find('table').find_all('tr')[1:]
            for row in rows:
                cols = row.find_all('td')
                if len(cols) < 3: continue
                try:
                    price = float(cols[2].text.strip().replace('$', '').split()[0])
                    all_vendors.append({
                        "name": cols[0].text.strip(),
                        "price": price,
                        "link": get_clean_link(cols[0].find('a')),
                        "zone": z['id'],
                        "state": z['state']
                    })
                except: continue
        except: continue

    if not all_vendors: return

    nh_pool = [v for v in all_vendors if v['state'] == "NH"]
    ma_pool = [v for v in all_vendors if v['state'] == "MA"]
    
    # ENSURE 128 OIL CANNOT WIN NH
    nh_winner = min(nh_pool, key=lambda x: x['price'])['name'] if nh_pool else ""
    ma_winner = min(ma_pool, key=lambda x: x['price'])['name'] if ma_pool else ""

    csv_row = {
        "date": current_time,
        "global_avg": round(sum(v['price'] for v in all_vendors) / len(all_vendors), 3),
        "NH_winner": nh_winner,
        "MA_winner": ma_winner,
        "NH_Zone_2_low": min([v['price'] for v in nh_pool if v['zone'] == 'NH_Zone_2'], default=""),
        "NH_Zone_6_low": min([v['price'] for v in nh_pool if v['zone'] == 'NH_Zone_6'], default=""),
        "MA_Zone_9_low": min([v['price'] for v in ma_pool if v['zone'] == 'MA_Zone_9'], default=""),
        "full_data": json.dumps(all_vendors)
    }

    with open('vendors.json', 'w') as f: json.dump(all_vendors, f)
    file_exists = os.path.isfile('data.csv')
    with open('data.csv', 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=csv_row.keys())
        if not file_exists: writer.writeheader()
        writer.writerow(csv_row)

if __name__ == "__main__": scrape()

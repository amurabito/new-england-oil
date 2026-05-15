import requests
from bs4 import BeautifulSoup
import json, csv, os
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# CONFIGURATION & STATE GUARD
ZONES = [
    {"url": "https://www.newenglandoil.com/massachusetts/zone9.asp?x=0", "id": "MA_Zone_9", "state": "MA"},
    {"url": "https://www.newenglandoil.com/newhampshire/zone2.asp?x=0", "id": "NH_Zone_2", "state": "NH"},
    {"url": "https://www.newenglandoil.com/newhampshire/zone6.asp?x=0", "id": "NH_Zone_6", "state": "NH"}
]

def get_clean_link(a_tag, base_url):
    """
    Correctly resolves relative links by prepending domain and state-specific subdirectories.
    Handles standard URLs, 'click.asp' redirects, and relative paths.
    """
    if not a_tag or not a_tag.get('href'):
        return "#"
    
    href = a_tag['href'].strip()
    
    # 1. Handle absolute URLs
    if href.startswith('http'):
        return href
        
    # 2. Handle internal 'click.asp' redirects if present
    if 'click.asp' in href:
        params = parse_qs(urlparse(href).query)
        if 'x' in params:
            return params['x'][0]

    # 3. Handle relative paths by identifying state context from base_url
    clean_href = href.lstrip('/')
    if 'massachusetts' in base_url:
        return f"https://www.newenglandoil.com/massachusetts/{clean_href}"
    elif 'newhampshire' in base_url:
        return f"https://www.newenglandoil.com/newhampshire/{clean_href}"
    
    # Fallback
    return f"https://www.newenglandoil.com/{clean_href}"

def scrape():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    all_vendors = []
    
    for z in ZONES:
        try:
            print(f"Scraping {z['id']}...")
            res = requests.get(z['url'], timeout=15)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # The vendors are typically in a table; we target the rows while skipping headers
            # Adjusting selector to be robust based on typical site structure
            table = soup.find('table')
            if not table:
                continue
                
            rows = table.find_all('tr')[1:] # Skip header row
            
            for row in rows:
                cols = row.find_all('td')
                if len(cols) < 3:
                    continue
                
                try:
                    # Clean vendor name
                    name = cols[0].get_text(strip=True)
                    if not name:
                        continue
                        
                    # Extract and clean price
                    price_text = cols[2].get_text(strip=True).replace('$', '').split()[0]
                    price = float(price_text)
                    
                    # Resolve link using the fixed logic
                    link = get_clean_link(cols[0].find('a'), z['url'])
                    
                    all_vendors.append({
                        "name": name,
                        "price": price,
                        "link": link,
                        "zone": z['id'],
                        "state": z['state']
                    })
                except (ValueError, IndexError) as e:
                    continue
                    
        except Exception as e:
            print(f"Error scraping {z['id']}: {e}")

    if not all_vendors:
        print("No vendor data found.")
        return

    # Segment pools for state-specific winner logic (The State Guard)
    nh_pool = [v for v in all_vendors if v['state'] == "NH"]
    ma_pool = [v for v in all_vendors if v['state'] == "MA"]
    
    nh_winner = min(nh_pool, key=lambda x: x['price'])['name'] if nh_pool else "Unknown"
    ma_winner = min(ma_pool, key=lambda x: x['price'])['name'] if ma_pool else "Unknown"

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

    # Save current state for frontend immediate view
    with open('vendors.json', 'w') as f:
        json.dump(all_vendors, f)
    
    # Append to historical CSV
    file_exists = os.path.isfile('data.csv')
    with open('data.csv', 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=csv_row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(csv_row)
    
    print(f"Scrape completed successfully at {current_time}")

if __name__ == "__main__":
    scrape()

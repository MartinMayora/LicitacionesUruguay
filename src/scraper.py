import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from typing import List, Dict
import time
import csv
import os

def scrape_contrataciones_uruguay(date_string: str) -> List[Dict]:
    try:
        target_date = datetime.strptime(date_string, '%d-%m-%Y')
    except ValueError:
        raise ValueError("Invalid date format. Please use DD-MM-YYYY format (e.g., '29-09-2025')")
    
    print(f"Looking for calls with publication date: {date_string}")
    print("Will start collecting when first target date is found, stop when older dates are found")
    
    llamados = []
    page = 1
    max_pages = 50
    found_older_dates = False
    started_collecting = False  
    
    while page <= max_pages and not found_older_dates:
        print(f"Checking page {page}...")
        
        page_llamados, has_next_page, older_dates_found, found_target_date = scrape_single_page(page, target_date, started_collecting)
        
        if found_target_date and not started_collecting:
            started_collecting = True
            print(f"First occurrence of {date_string} found on page {page}, starting collection...")
        
        if started_collecting:
            llamados.extend(page_llamados)
            print(f"Collected {len(page_llamados)} calls from page {page}")
        else:
            print(f"Skipping page {page} (haven't reached target date yet)")
        
        if older_dates_found:
            found_older_dates = True
            print(f"Found dates older than {date_string}, stopping search.")
            break
        
        if not has_next_page:
            print("Reached the last page")
            break
        
        page += 1
        time.sleep(0.5)
    
    if started_collecting:
        print(f"Finished! Total calls collected: {len(llamados)}")
    else:
        print(f"No calls found for date {date_string}")
    
    return llamados

def scrape_single_page(page: int, target_date: datetime, started_collecting: bool) -> tuple:
    if page == 1:
        url = "https://contratacionesuruguay.com/convocatorias-nacionales.html"
    else:
        url = f"https://contratacionesuruguay.com/convocatorias-nacionales-{page}.html"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        has_next_page = check_pagination(soup, page)
        
        tables = soup.find_all('table')
        
        page_llamados = []
        found_older_dates = False
        found_target_date = False
        
        for table in tables:
            rows = table.find_all('tr')
            
            for row in rows:
                if row.find('th'):
                    continue
                
                cells = row.find_all('td')
                if len(cells) < 9:
                    continue
                
                publication_cell = cells[7].get_text(strip=True)
                publication_date_match = re.match(r'(\d{2}-\d{2}-\d{4})', publication_cell)
                
                if publication_date_match:
                    publication_date_str = publication_date_match.group(1)
                    
                    try:
                        publication_date = datetime.strptime(publication_date_str, '%d-%m-%Y')
                        
                        if publication_date == target_date and not found_target_date:
                            found_target_date = True
                        
                        if publication_date < target_date:
                            found_older_dates = True
                            continue
                        
                        if started_collecting and publication_date >= target_date:
                            llamado_info = extract_llamado_info_from_row(cells, publication_date_str)
                            if llamado_info:
                                page_llamados.append(llamado_info)
                                
                    except ValueError:
                        if started_collecting:
                            llamado_info = extract_llamado_info_from_row(cells, publication_date_str)
                            if llamado_info:
                                page_llamados.append(llamado_info)
        
        return page_llamados, has_next_page, found_older_dates, found_target_date
        
    except requests.RequestException as e:
        print(f"Error fetching page {page}: {e}")
        return [], False, False, False
    except Exception as e:
        print(f"Error parsing page {page}: {e}")
        return [], False, False, False

def check_pagination(soup, current_page: int) -> bool:

    next_links = soup.find_all('a', href=re.compile(r'convocatorias-nacionales-\d+\.html'))
    
    for link in next_links:
        href = link.get('href', '')
        # Extract page number from href like "convocatorias-nacionales-5.html"
        page_match = re.search(r'convocatorias-nacionales-(\d+)\.html', href)
        if page_match:
            page_num = int(page_match.group(1))
            if page_num > current_page:
                return True
    
    # Also check for "Siguiente" or "Next" links
    next_text_links = soup.find_all('a', string=re.compile(r'siguiente|next|>|»', re.IGNORECASE))
    if next_text_links:
        for link in next_text_links:
            href = link.get('href', '')
            if href and not href.endswith('#') and 'convocatorias-nacionales' in href:
                return True
    
    # Check for page numbers in the text content
    pagination_text = soup.get_text()
    if f"convocatorias-nacionales-{current_page + 1}.html" in pagination_text:
        return True
    
    return False

def extract_llamado_info_from_row(cells, publication_date: str) -> Dict:
    """
    Extract specific information from a table row.
    """
    try:
        info = {
            'link': '',
            'entidad': '',
            'unidad_ejecutora': '',
            'objeto': '',
            'nro_llamado': '',
            'fecha_publicacion': '',
            'fecha_apertura': '',
            'estado': '',
            'modalidad': '',
            'id': ''
        }
        
        # Extract information using the known column indices:
        # 0: ID, 1: ENTIDAD, 2: UNIDAD EJECUTORA, 3: OBJETO, 4: ESTADO, 
        # 5: Nro LLAMADO, 6: MODALIDAD, 7: PUBLICACION, 8: APERTURA
        
        # ID (Nro)
        info['id'] = cells[0].get_text(strip=True)
        
        # Entity
        info['entidad'] = cells[1].get_text(strip=True)
        
        # Execution Unit
        info['unidad_ejecutora'] = cells[2].get_text(strip=True)
        
        # Object
        info['objeto'] = cells[3].get_text(strip=True)
        
        # Status
        info['estado'] = cells[4].get_text(strip=True)
        
        # Call Number
        info['nro_llamado'] = cells[5].get_text(strip=True)
        
        # Modality
        info['modalidad'] = cells[6].get_text(strip=True)
        
        # Publication date
        info['fecha_publicacion'] = cells[7].get_text(strip=True)
        
        # Apertura date
        info['fecha_apertura'] = cells[8].get_text(strip=True)
        
        for cell in cells:
            link_tag = cell.find('a', href=True)
            if link_tag:
                href = link_tag['href']
                if href.startswith('/'):
                    info['link'] = f"https://contratacionesuruguay.com{href}"
                elif href.startswith('http'):
                    info['link'] = href
                else:
                    info['link'] = f"https://contratacionesuruguay.com/{href}"
                break
        
        if not info['link'] and info['id']:
            info['link'] = f"https://contratacionesuruguay.com/llamado-{info['id']}"
        
        return info
        
    except Exception as e:
        print(f"Error extracting llamado info from row: {e}")
        return None

def save_to_csv(llamados: List[Dict], filename: str = None):
    """
    Save the scraped data to a CSV file.
    
    Args:
        llamados: List of procurement call dictionaries
        filename: Output filename (optional, will auto-generate if not provided)
    """
    if not llamados:
        print("No data to save to CSV.")
        return None
    
    if not filename:
        filename = os.path.join(os.path.dirname(os.path.dirname(__file__)), "build", "licitaciones.csv")    
    try:
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        fieldnames = [
            'id', 
            'entidad', 
            'unidad_ejecutora', 
            'objeto', 
            'nro_llamado', 
            'fecha_publicacion', 
            'fecha_apertura', 
            'estado', 
            'modalidad', 
            'link'
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for llamado in llamados:
                row = {field: llamado.get(field, '') for field in fieldnames}
                writer.writerow(row)
        
        print(f"Data successfully saved to: {filename}")
        print(f"Total records saved: {len(llamados)}")
        
        file_path = os.path.abspath(filename)
        print(f"File location: {file_path}")
        
        return filename
        
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return None

def print_results(llamados: List[Dict]):
    """Print the results in a formatted way."""
    if not llamados:
        print("No procurement calls found for the specified date range.")
        return
    
    print(f"\nFound {len(llamados)} procurement call(s):")
    print("=" * 100)
    
    calls_by_date = {}
    for llamado in llamados:
        date = llamado.get('fecha_publicacion', 'Unknown').split()[0]
        if date not in calls_by_date:
            calls_by_date[date] = []
        calls_by_date[date].append(llamado)
    
    for date in sorted(calls_by_date.keys()):
        print(f"\nDate: {date}")
        print("-" * 50)
        for i, llamado in enumerate(calls_by_date[date], 1):
            print(f"  {i}. {llamado.get('entidad', 'N/A')} - {llamado.get('objeto', 'N/A')}")
            print(f"     Call Number: {llamado.get('nro_llamado', 'N/A')}")
            print(f"     Execution Unit: {llamado.get('unidad_ejecutora', 'N/A')}")
            print(f"     Link: {llamado.get('link', 'N/A')}")


from scraper import scrape_contrataciones_uruguay, save_to_csv
from parseCSV import parseCSV, printParsedList
from prompt import intrested_in_licitacion, result_to_csv
from licitaciones import process_licitaciones
from send_email import send_email_with_csv

def get_licitaciones_send_email(date):
    date_to_scrape = date
    results = scrape_contrataciones_uruguay(date_to_scrape)
    path = save_to_csv(results)
    parsedCSV = parseCSV(path)
    printParsedList(parsedCSV)
    list_intresting = process_licitaciones(parsedCSV)
    filename = result_to_csv(list_intresting)
    send_email_with_csv(filename, "martinmayora@gmail.com", date)

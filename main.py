from scraper import scrape_contrataciones_uruguay, save_to_csv
from parseCSV import parseCSV, printParsedList
from prompt import intrested_in_licitacion, result_to_csv
if __name__ == "__main__":
    date_to_scrape = "30-09-2025"
    results = scrape_contrataciones_uruguay(date_to_scrape)
    path = save_to_csv(results)
    parsedCSV = parseCSV(path)
    printParsedList(parsedCSV)
    list_intresting = [(parsedCSV[0][1],parsedCSV[0][2])]
    #for parse in parsedCSV:
    #    result = intrested_in_licitacion(parse[0])
    #    if result == "SI":
    #        list_intresting.append((parse[1],parse[2]))
    filename = result_to_csv(list_intresting)


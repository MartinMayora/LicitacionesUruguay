import csv 

def parseCSV(pathCSV):
    parsedList = []
    with open(pathCSV, newline = '') as csvfile:
        parser = csv.DictReader(csvfile)
        for row in parser:
            toAdd = f'Entidad: {row['entidad']} Unidad Ejecutora: {row['unidad_ejecutora']} Objeto: {row['objeto']}'
            parsedList.append((toAdd, row['id'], row['link']))

    return parsedList

def printParsedList(parsedList):
    print("=" * 80)
    print("PARSED LIST CONTENTS:")
    print("=" * 80)
    
    for i, item in enumerate(parsedList, 1):
        toAdd, item_id, link = item
        print(f"Item {i}:")
        print(f"  Summary: {toAdd}")
        print(f"  ID: {item_id}")
        print(f"  Link: {link}")
        print("-" * 80)

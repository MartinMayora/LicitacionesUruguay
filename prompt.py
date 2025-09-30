import requests
from dotenv import load_dotenv
import os
import csv
load_dotenv()

def intrested_in_licitacion(licitacion):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={os.getenv('GEMINI_API_KEY')}"
    
    prompt = f"""Sos un analista que puede determinar si cierta licitacion es interesante para mi compania.
    Mi compania es de software y tenemos un gran equipo, entonces todo tipo de licitacion sobre software o tecnologia nos interesa.
    
    LICITACION PARA ANALIZAR:
    {licitacion}
    
    SOLO responder con "SI" o "NO". No agregar ningun tipo de explicacion ni informacion adicional."""

    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 10,
            "topK": 1
        }
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text'].strip()
        else:
            print(f"API Error: {response.text}")
            return "ERROR"
            
    except Exception as e:
        print(f"Error: {e}")
        return "ERROR"

def result_to_csv(list_intresting):  # Parameter name is list_intresting
    filename = "licitacionesInteresantes.csv"
    
    try:
        # Define the field order for the CSV
        fieldnames = ['id', 'link']
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write data rows - FIXED: use list_intresting instead of licitaciones_data
            # Convert tuples to dictionaries
            for licitacion in list_intresting:
                # Assuming each licitacion is a tuple: (id, link)
                row_dict = {
                    'id': licitacion[0],
                    'link': licitacion[1]
                }
                writer.writerow(row_dict)
        
        print(f"Successfully saved {len(list_intresting)} records to {filename}")
        return filename
        
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return None

if __name__ == "__main__":
    test_licitacion = 'Entidad: "Ministerio de Tecnología" Unidad Ejecutora: "Dirección de Sistemas" Objeto: "Desarrollo de software de gestión"'
    result = intrested_in_licitacion(test_licitacion)
    list_r = [result]
    result_to_csv(list_r)
    print("Final Result:", result)
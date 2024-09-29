import library 
from library import Scraping_Maps

def main():
    search_terms = input("Ingrese el tipo de negocio a buscar: ")
    if search_terms is None:
        print("No se ingreso el tipo de negocio")
    else:
        if len(search_terms) == 1:
            search_terms = [search_terms]   
        for i in search_terms:
            url = fr"https://www.google.es/maps/search/{i}/"
            Scraping_Maps(url)

if __name__ == '__main__':
   main()
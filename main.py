import library 
from library import Scraping_Maps

def main():
    while True:
        search_terms = input("Ingrese el tipo de negocio a buscar: ")
        if search_terms is None:
            print("No se ingreso el tipo de negocio")
        else:
            if type(search_terms) == str:
                url = fr"https://www.google.es/maps/search/{search_terms}/"
                Scraping_Maps(url)
            else:
                for i in search_terms:
                    url = fr"https://www.google.es/maps/search/{i}/"
                    Scraping_Maps(url)
            break

if __name__ == '__main__':
    main()
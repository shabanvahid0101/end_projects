from countryinfo import CountryInfo
country=CountryInfo(input("enter country name : "))

capital =country.capital()
population =country.population() 
area = country.area()
region =country.region()
subregion=country.subregion()
demonym=country.demonym()
currency=country.currencies()
languages=country.languages()
borders=country.borders()
print(f'capital : {capital}\n population : {population}\n area : {area}\n region: {region}\n subregion : {subregion}\n demonym {demonym}\n currency : {currency}\n languages : {languages}\n borders : {borders}')

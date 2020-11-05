
# imports
from bs4 import BeautifulSoup 
from selenium import webdriver
import requests 
import pandas as pd
import time 

driver= webdriver.Firefox(executable_path=r"/home/alexis/Documents/geckodriver")


def get_url(driver,url):
    driver.get(url)



def get_locations(driver,url):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(url)
    time.sleep(15)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

url="https://farmatodo.com.ve/categorias/belleza/cosmeticos"

get_url(driver,url)

#tiempo de espera le puse 10 seg porque mi internet no es tan rapido
time.sleep(10)


#aqui tiene que estar el scroll
scroll_pause_time = 10





#extraigo los elementos que estan en las cartas 
elements=driver.find_elements_by_xpath("/html/body/app-root/div/div[2]/app-categories/div/div[3]/div[2]/div[2]/div/app-group-view/div/div/div[2]/div")



cards=[]
#guardo los cards que estan en la pagina 
for e in elements:
    cards.append(e)

#extraigo el html de cada card para su analisis y extraccion de datos

images=list()
names=list()
description=list()
prices=list()
disp=list()
urlProduct=list()
#estudiando la pagina agarramos el url dde busqueda que usa farmatodo 
urlSearch='https://farmatodo.com.ve/buscar?producto='

#para cada card se extrae su informacion 
for c in cards:
    #convierto el elemento de selenium y extraigo su html
    page=c.get_attribute('innerHTML')
    pageSoup= BeautifulSoup(page,'html.parser')
    #extraemos la imagen
    picture=pageSoup.find('img',class_='image')
    images.append(picture['src'])
    #extraemos el nombre 
    name=pageSoup.find('p',class_='text-title')
    names.append(name.text)
    #extraemos la descripcion 
    descr=pageSoup.find('p',class_='text-description')
    description.append(descr.text)
    #extraemos el precio
    pric=pageSoup.find('span',class_='text-price')
    prices.append(pric.text.replace('Bs. ',''))
    #extraemos la disponibilidad
    dis=pageSoup.find('p',class_='petal-text')
    disp.append(dis.text)
    #extraemos el url para la busqueda directa del producto 
    #aqui quitamos los escios en blanco del nombre para la busqueda
    urlProduct.append(urlSearch + '' +  name.text.replace(" ", "%20") +'&departamento=Todos&filtros=')

time.sleep(15)
numCities=list()
mainCity=list()
cont=0
#se abre una nueva pestaña con cada producto y se hace click para extraer su inf de locacion 
for url in urlProduct:
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(url)
    time.sleep(15)
    element=driver.find_elements_by_xpath("/html/body/app-root/div/div[2]/app-algolia/div/div/div/app-group-view/div/div[2]/div[2]/div[1]")
    element[0].click()
    time.sleep(15)
    #aqui se recoge la info de la ubicacion
    #convierto el elemento de selenium y extraigo su html
    page=driver.page_source
    pageSoup= BeautifulSoup(page,'html.parser') 
    
    #se extrae el numero de ciudades
    #cities=pageSoup.find('div',class_='ng-star-inserted')
    maincity=pageSoup.find('h6',class_='text-city')
    print(maincity)
    #numCities.append(str(len(cities)))
    #se extrae la ciudad principal 
    mainCity.append(maincity.text)
    time.sleep(15)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])



print (mainCity)

print(numCities)

#aqui extraeremos los datos de ubicacion del proeducto




#transformamos toda la data que recogimos y la metemos en el csv 
df=pd.DataFrame({'Name':names,'Description':description,'Prices':prices,'Availability':disp,'Image':images,'URL':urlProduct,'Main':mainCity})

#print(df)

#salvamos el csv 
df.to_csv('farmatodo_belleza_cosmeticos2.csv')



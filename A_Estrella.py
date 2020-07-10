import pygame
import math 

distancias_bucarest = {'Arad':366,'Bucarest':0,'Craiova':160,'Dobreta':242,
                       'Eforie':161,'Fagaras':176,'Giorgiu':77,'Hirsova':151,
                       'Iasi':226,'Lugoj':244,'Mehadia':241,'Neamt':234,
                       'Oradea':380,'Pitesti':100,'Rimnicu Vilcea':193,'Sibiu':253,
                       'Timisoara':329,'Urziceni':80,'Vaslui':199,'Zerind':374}

ubicaciones = {'Arad':(140,180),'Bucarest':(498, 344),'Craiova':(315, 386),'Dobreta':(195, 380),
               'Eforie':(624, 405),'Fagaras':(372, 200),'Giorgiu':(445, 416),'Hirsova':(628, 309),
               'Iasi':(495, 132),'Lugoj':(213, 300),'Mehadia':(212, 337),'Neamt':(429, 108),
               'Oradea':(182, 93),'Pitesti':(388, 290),'Rimnicu Vilcea':(297, 249),'Sibiu':(255, 187),
               'Timisoara':(141, 264),'Urziceni':(537, 305),'Vaslui':(555, 201),'Zerind':(151, 133)}


grafo = {"Oradea":{"Zerind":(71,6,4),"Sibiu":(151,6,3)},
       "Zerind":{"Oradea":(71,6,4),"Arad":(75,6,5)},
       "Arad":{"Zerind":(75,6,5),"Sibiu":(140,5,4),"Timisoara":(118,5,3)},
       "Sibiu":{"Oradea":(151,6,3),"Arad":(140,5,4),"Fagaras":(99,7,2),"Rimnicu Vilcea":(80,6,2)},
       "Timisoara":{"Arad":(118,5,3),"Lugoj":(111,6,3)},
       "Lugoj":{"Timisoara":(111,6,3),"Mehadia":(70,4,4)},
       "Mehadia":{"Lugoj":(70,4,4),"Dobreta":(75,4,3)},
       "Dobreta":{"Mehadia":(75,4,3),"Craiova":(120,7,3)},
       "Craiova":{"Dobreta":(120,7,3),"Rimnicu Vilcea":(146,8,1),"Pitesti":(138,6,4)},
       "Rimnicu Vilcea":{"Sibiu":(80,6,2),"Craiova":(146,8,1),"Pitesti":(97,7,2)},
       "Pitesti":{"Craiova":(138,6,4),"Rimnicu Vilcea":(97,7,2),"Bucarest":(101,8,1)},
       "Fagaras":{"Sibiu":(99,7,2),"Bucarest":(211,8,3)},
       "Bucarest":{"Fagaras":(211,8,3),"Pitesti":(101,8,1),"Giorgiu":(90,8,1),"Urziceni":(85,9,2)},
       "Giorgiu":{"Bucarest":(90,8,1)},
       "Urziceni":{"Bucarest":(85,9,2),"Hirsova":(98,7,4),"Vaslui":(142,5,2)},
       "Hirsova":{"Urziceni":(98,7,4),"Eforie":(86,7,3)},
       "Eforie":{"Hirsova":(86,7,3)},
       "Vaslui":{"Urziceni":(142,5,2),"Iasi":(92,7,4)},
       "Iasi":{"Vaslui":(92,7,4),"Neamt":(87,5,3)},
       "Neamt":{"Iasi":(87,5,3)}
       }      

# ------- Implementacion A* --------------------------

class Nodo:
    def __init__(self, nombre="", padre=""):
        self.nombre = nombre
        self.padre = padre
        self.g = 0 
        self.h = 0
        self.f = 0 

    def __eq__(self, nodo):
        return self.nombre == nodo.nombre

    def __lt__(self, nodo):
         return self.f < nodo.f


def algoritmo(inicio, fin):
    
    nodos_abiertos = []
    nodos_cerrados = []

    nodo_inicial = Nodo(inicio, None)
    nodo_final = Nodo(fin, None)
    nodos_abiertos.append(nodo_inicial)
    
    while len(nodos_abiertos) > 0:
        nodos_abiertos.sort()
        nodo_actual = nodos_abiertos.pop(0)
        nodos_cerrados.append(nodo_actual)

        if nodo_actual == nodo_final:
            ruta = []
            while nodo_actual != nodo_inicial:
                ruta.append(nodo_actual.nombre)
                nodo_actual = nodo_actual.padre
            ruta.append(nodo_inicial.nombre)
            ruta.reverse()
            return ruta

        vecinos = grafo.get(nodo_actual.nombre)
        for key, value in vecinos.items():
            vecino = Nodo(key, nodo_actual)

            if(vecino in nodos_cerrados):
                continue
            vecino.g = nodo_actual.g + costo_entre_nodos(grafo.get(nodo_actual.nombre).get(vecino.nombre))
            vecino.h = heuristica(vecino.nombre)
            vecino.f = vecino.g + vecino.h

            if(agregar_abiertos(nodos_abiertos, vecino) == True):
                nodos_abiertos.append(vecino)

    return None

def costo_entre_nodos(argumentos):
    distancia = argumentos[0]
    carretera = (argumentos[1]*220)/10
    peligro = argumentos[2]    
    return ((2/3)*distancia - (1/3)*carretera) * peligro

def heuristica(ciudad):
    ciudades = grafo[ciudad]
    suma = 0
    for nombre_ciudad in list(ciudades):
        suma += ciudades[nombre_ciudad][2]
        
    promedio_peligro = (suma/len(ciudades))
    
    return distancias_bucarest[ciudad] * promedio_peligro
    
def agregar_abiertos(nodos_abiertos, vecino):
    for nodo in nodos_abiertos:
        if (vecino == nodo and vecino.f > nodo.f):
            return False
    return True


# ------- Interfaz Grafica --------------------------

def mensaje(ventana):
    font = pygame.font.Font("freesansbold.ttf", 26)  
    text = font.render("Seleccione el punto de partida hacia Bucharest", 1, (0, 0, 0))
    ventana.blit(text, (80,20))
    
def dibujar_circulo(ventana,pos):
    color = (220,20,60)
    pygame.draw.circle(ventana, color, pos, 10)

def dibujar_linea(ventana,punto1,punto2):
    color = (220,20,60)
    pygame.draw.line(ventana, color, punto1, punto2,5)
    pygame.display.flip()
    
def click_ciudad(pos):
    rango = 12
    for ciudad in list(ubicaciones):
        ubicacion = (ubicaciones.get(ciudad))
        if(pos[0]>(ubicacion[0]-rango) and pos[0]<(ubicacion[0]+rango)) and (pos[1]>(ubicacion[1]-rango) and pos[1]<(ubicacion[1]+rango)):
              return ciudad
            
    return None

def mostrar_estadisticas(ruta,ventana):
    distancia = 0
    carretera = 0
    peligro = 0
    
    for i in range(len(ruta)):
        if(i<len(ruta)-1):
            argumentos = grafo.get(ruta[i]).get(ruta[i+1])
            distancia += argumentos[0]
            carretera += argumentos[1]
            peligro += argumentos[2]

    n_rutas = len(ruta)-1      
    peligro =  math.trunc(((peligro/n_rutas)*10))
    carretera = math.trunc(((carretera/n_rutas)*100)/10)
    
    font = pygame.font.Font("freesansbold.ttf", 16)  
    text = font.render("Distancia: "+str(distancia)+"km", 1, (0, 0, 0))
    ventana.blit(text, (50,470))
    
    text = font.render("Peligrosidad: "+str(peligro)+"%", 1, (0, 0, 0))
    ventana.blit(text, (350,470))
    
    text = font.render("Estado de la carretera: "+str(carretera)+"%", 1, (0, 0, 0))
    ventana.blit(text, (50,490))        
            
def main():
    pygame.init()
    ventana = pygame.display.set_mode((750,520),0,32)
    pygame.display.set_caption("Algoritmo A*")
    ventana.fill((255,255,255))
    relog = pygame.time.relog()
    fondo = pygame.image.load(r'fondo.jpg')
    ventana.blit(fondo, (0, 0))
    mensaje(ventana)
    mapa_imagen = pygame.image.load(r'mapa.jpg')
    area_mapa = ventana.blit(mapa_imagen, (50, 50)) 
    termino_ejecucion = False
    mostrandoRuta = False
    while not termino_ejecucion:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if area_mapa.collidepoint(pos):
                    inicio = (click_ciudad(pos))
                    if(inicio!=None):
                        if(mostrandoRuta):
                            ventana.blit(fondo, (0, 0))
                            mensaje(ventana)
                            ventana.blit(mapa_imagen, (50, 50))
                            
                        ruta = algoritmo(inicio, 'Bucarest')
                        mostrar_estadisticas(ruta,ventana)
                        for i in range(len(ruta)):
                            punto1 = ubicaciones.get(ruta[i])
                            dibujar_circulo(ventana,punto1)
                            if i<len(ruta)-1:                            
                                punto2 = ubicaciones.get(ruta[i+1])
                                dibujar_linea(ventana,punto1,punto2)
                        mostrandoRuta=True        

            if event.type == pygame.QUIT:
                termino_ejecucion = True

            if event.type == pygame.KEYDOWN:
                if(event.key==27):
                    termino_ejecucion = True
                    
        pygame.display.update()
        relog.tick(10)             

    pygame.quit()
    
if __name__ == "__main__": main()

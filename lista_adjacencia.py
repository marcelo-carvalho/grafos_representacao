# Algoritmos em grafos
# Engenharia de Computação Noturno
# Atividade 1 - Estrutura para representação de grafos 
# Aluno: Marcelo de Carvalho Pereira    Matricula: 687921
#
# A bibliiteca tkinter é fundamental para o funcionamento do programa
# gentileza se certificar de que a mesma incranta-se disponível 


from collections import deque
import queue
from tkinter import * 
from tkinter import filedialog
from tkinter import messagebox

class Grafo:
    #construtor
    def __init__(self, num_vertices):
        self.c_num_vertices = num_vertices
        self.c_vertices = range(self.c_num_vertices)                                #determina dimensão da lista

        self.c_lista_adj = {vertice: set() for vertice in self.c_vertices}          #cria estrutura lista para sucessores
        self.c_lista_adj_ant = {vertice: set() for vertice in self.c_vertices}      #cria estrutura lista para antecessores

    #adiciona pares de vertices as estruturas de dados
    def adiciona_aresta(self, vertice_1, vertice_2):
        self.c_lista_adj[vertice_1].add(vertice_2)                                  #adiciona elemento na lista de sucessores
        self.c_lista_adj_ant[vertice_2].add(vertice_1)                              #adiciona elemento na lista de antecessores

    #pega elemento sucessores de um vértice
    def get_sucessores(self,vertice):
        try:
            if(vertice <= 0):
                raise Exception("Vérice deve ser maior que 0.")
            return self.c_lista_adj[vertice]
        except:
            raise Exception("Valor inválido ou fora dos limites do grafo.")  #exceção para valor inválido
    
    #pega elemento antecessores de um vértice
    def get_antecessores(self,vertice):
        try:
            if(vertice <= 0):
                raise Exception("Vérice deve ser maior que 0.")
            return self.c_lista_adj_ant[vertice]
        except:
            raise Exception("Valor inválido ou fora dos limites do grafo.")   #exceção para valor inválido

    #pega grau de sucessores
    def get_grau_sucessores(self,vertice):
        try:
            if(vertice <= 0):
                raise Exception("Vérice deve ser maior que 0.")
            return len(self.c_lista_adj[vertice])
        except:
            raise Exception("Valor inválido ou fora dos limites do grafo.")    #exceção para valor inválido
    
    #pega grau de antecessores
    def get_grau_antcessores(self,vertice):
        try:
            if(vertice <= 0):
                raise Exception("Vérice deve ser maior que 0.")
            return len(self.c_lista_adj_ant[vertice])
        except:
            raise Exception("Valor inválido ou fora dos limites do grafo.")     #exceção para valor inválido
    
    def get_num_vertices(self):
        return int(self.c_num_vertices)

    def get_vertices(self):
        return self.c_lista_adj
    
    #Busca em Profundidade 
    def busca_profundidade(self,vertice,visitados):
        visitados.append(vertice)                                               #Inicia pilha com vértice escolhido pelo usuário
        for vizinho in self.c_lista_adj[vertice]:
            if vizinho not in visitados:
                self.busca_profundidade(vizinho,visitados)

    #Busca e Largura
    def busca_largura(self,vertice,visitados):
        fila = [vertice]                                                        #Inicia fila com vértice escolhido pelo usuário
        while fila:
            visitar = fila.pop(0)
            if visitar not in visitados:
                visitados.append(visitar)
                vizinhos = list(self.get_sucessores(visitar))
                fila.extend(vizinhos)
    
    def encontra_caminho(self,node1,node2,path=[]):
        
        if node1 and node2 not in self.get_vertices():
            return None
        if(node2 in path):
            return path
        else:
            path.append(node1)
        for vizinho in self.c_lista_adj[node1]:
            if vizinho not in path:
                self.encontra_caminho(vizinho,node2,path)
        return path

    def encontra_caminho_quase(self,src, dest):
        n = self.get_num_vertices()
        discovered = [False] * n
        q = deque()
        discovered[src] = True
        q.append(src)

        while q:
            v = q.popleft()
            if v == dest:
                return True

            for u in self.c_lista_adj[v]:
                if not discovered[u]:
                    discovered[u] == True
                    q.append(u)
        return False
    
    def encontra_caminho_errado(self,source,destination,visited=None):
        if source == destination:
            return [destination]
        else:
            visited = visited or set()
            for new_source in self.c_lista_adj[source]:
                if new_source not in visited:
                    visited.add(new_source)
                    sub_path = self.encontra_caminho(new_source,destination,visited)
                    if sub_path is not None:
                        return [source] + sub_path
    
    def eh_conexo(self):
        dps =list()
        self.busca_profundidade(1,dps)
        if len(dps) == len(self.c_lista_adj):
            return True
        else:
            return False


#Classe para geração da janela 
class Tela:
    def __init__(self, master):
        self.mainTela = master
        self.mainTela.title("Grafos")
        self.mainTela.geometry('400x600')

        # Particição da Janela para diferentes agrupamentos de widgets
        self.frame_cima = Frame(self.mainTela).grid()
        self.frame_baixo = Frame(self.mainTela).grid()

        # Cria um título
        self.lableTitulo = Label(self.frame_cima, text="Atividade 1 - Representação de Grafos")
        self.lableTitulo.grid(column=2, row=1)
        
        # Widgets para importação do Arquivo
        self.graph = None
        self.arquivo_importado = False
        self.lable1 = Label(self.frame_cima, text="Arquivo de entrada: ")
        self.lable1.grid(column=1, row=3,sticky="W")
        self.caminho_arquivo = StringVar()
        self.entry1 = Entry(self.frame_cima, textvariable=self.caminho_arquivo)
        self.entry1.grid(column=2, row=3,sticky="W")
        self.botaoCarregar = Button(self.frame_cima, text="...", command=self.carrega_arquivo)
        self.botaoCarregar.grid(column=3, row=3,sticky="W")

        # Widgets para a função de Busca Aresta
        self.lable2 = Label(self.frame_cima, text="Vértice: ")
        self.lable2.grid(column=1, row=4,sticky="W")
        self.entry2 = Entry(self.frame_cima)
        self.entry2.grid(column=2, row=4,sticky="W")
        self.botaoCarregar = Button(self.frame_cima, text="Buscar", command=self.busca_vertice)
        self.botaoCarregar.grid(column=3, row=4,sticky="W")

        #Widgets para busca em profundidade
        self.labelBuscaProfundidade = Label(self.frame_cima, text="Vértice: ")
        self.labelBuscaProfundidade.grid(column=1,row=14,stick="W")
        self.entryBuscaProfundidade = Entry(self.frame_cima)
        self.entryBuscaProfundidade.grid(column=2,row=14,stick="W")
        self.botaoBuscaProfundidade = Button(self.frame_cima, text="Busca Profundidade", command=self.busca_profundidade)
        self.botaoBuscaProfundidade.grid(column=3,row=14)

        #Widgets para busca em largura
        self.labelBuscaLargura = Label(self.frame_cima, text="Vértice: ")
        self.labelBuscaLargura.grid(column=1,row=16,stick="W")
        self.entryBuscaLargura = Entry(self.frame_cima)
        self.entryBuscaLargura.grid(column=2,row=16,stick="W")
        self.botaoBuscaLargura = Button(self.frame_cima, text="Busca Largura", command=self.busca_largura)
        self.botaoBuscaLargura.grid(column=3,row=16)

        #Widgets para buscar caminho
        self.labelBuscaCaminho_1 = Label(self.frame_cima, text="Vértice Inicial: ")
        self.labelBuscaCaminho_1.grid(column=1,row=17,stick="W")
        self.entryBuscaCaminho_1 = Entry(self.frame_cima)
        self.entryBuscaCaminho_1.grid(column=2,row=17,stick="W")
        self.labelBuscaCaminho_2 = Label(self.frame_cima, text="Vértice Final: ")
        self.labelBuscaCaminho_2.grid(column=1,row=18,stick="W")
        self.entryBuscaCaminho_2 = Entry(self.frame_cima)
        self.entryBuscaCaminho_2.grid(column=2,row=18,stick="W")
        self.botaoBuscaCaminho = Button(self.frame_cima, text="Busca Caminho", command=self.busca_caminho)
        self.botaoBuscaCaminho.grid(column=2,row=19)

        # Widgets para apresentação dos Resultados
        self.Resultados = Label(self.frame_baixo, text="Resultados")
        self.Resultados.grid(column=2, row=5)
        self.label_Sucessores = Label(self.frame_baixo, text="Sucessores: ")
        self.label_Sucessores.grid(column=1, row=6,sticky="W")
        self.label_Grau_Sucessores = Label(self.frame_baixo, text="Grau Sucessores: ")
        self.label_Grau_Sucessores.grid(column=1, row=8,sticky="W")
        self.label_Antecessores = Label(self.frame_baixo, text="Antecessores: ")
        self.label_Antecessores.grid(column=1, row=10,sticky="W")
        self.label_Grau_Antecessores = Label(self.frame_baixo, text="Grau Sucessores: ")
        self.label_Grau_Antecessores.grid(column=1, row=12, sticky="W")
        self.Resultado_Sucessores = Label(self.frame_baixo, wraplength=180, text="")
        self.Resultado_Sucessores.grid(column=2, row=7,sticky="W")
        self.Resultado_Grau_Sucessores = Label(self.frame_baixo, wraplength=180, text="")
        self.Resultado_Grau_Sucessores.grid(column=2, row=9)     
        self.Resultado_Antecessores = Label(self.frame_baixo, wraplength=180, text="")
        self.Resultado_Antecessores.grid(column=2, row=11,sticky="W")
        self.Resultado_Grau_Antecessores = Label(self.frame_baixo, wraplength=180, text="")
        self.Resultado_Grau_Antecessores.grid(column=2, row=13)


    #Método para leitura e carregamentos dos dados nas estruturas de dados
    def carrega_arquivo(self):
        self.caminho_arquivo = filedialog.askopenfilename()
        self.entry1.delete(0,'end')
        self.entry1.insert(0,self.caminho_arquivo)
        
        try:
            with open(self.caminho_arquivo,'r') as file_object:     #testa se o arquivo pode ser aberto
                texto = file_object.readlines()                     #faz a leitura do arquivo texto
                texto2 = [linha.rstrip('\n') for linha in texto]    #separa os elementos por quebra de linha
                self.vertices = texto2[0].split()                   #separa os elementos da primeira linha
                self.graph = Grafo(int(self.vertices[0])+1)         #gria o grafo de acordo com as entradas da primeira linha
                for i in range(int(self.vertices[1])+1):            #loop para população da lista 
                    if i > 0:                                       #ignra a primeira linha
                        aresta = texto[i].split()
                        self.graph.adiciona_aresta(int(aresta[0]),int(aresta[1]))
                messagebox.showinfo(title="Loading", message="Grafo carregado com sucesso.")    #mensagem de carregamento positivo
                self.arquivo_importado = True                                                   #flag indicando a confirmação do carregamento, libera pesquisa
        except:
            messagebox.showerror("Falha", "Ocorreu um erro durante a leitura do grafo.")        #exceção caso há erro no carregamento
            self.arquivo_importado = False                                                      #flag indicando falha no carregamento, bloqueia pesquisa

    # Metódo para busca dos resultados nas estruturas de dados
    def busca_vertice(self):
        try:
            if(self.arquivo_importado == False):
                raise Exception("Arquivo não importado")                                        #se arquivo não importado gera exceção
            
            vertices_sucessores = self.graph.get_sucessores(int(self.entry2.get()))             #pega os elementos sucessores
            grau_sucessores = self.graph.get_grau_sucessores(int(self.entry2.get()))            #pega o grau de elementos sucessores
            vertices_antecessores = self.graph.get_antecessores(int(self.entry2.get()))         #pega os elementos antecessores
            grau_antecessores = self.graph.get_grau_antcessores(int(self.entry2.get()))         #pega o grau de elementos antecessores

            self.Resultado_Sucessores.configure(text=vertices_sucessores)                       #atualiza resultados com os elementos sucessores
            self.Resultado_Grau_Sucessores.configure(text=grau_sucessores)                      #atualiza resultados com o grau de elementos sucessores
            self.Resultado_Antecessores.config(text=vertices_antecessores)                      #atualiza resultados com os elementos antecessores
            self.Resultado_Grau_Antecessores.config(text=grau_antecessores)                     #atualiza resultados com o grau de elementos antecessores
        
        except Exception as e:
            messagebox.showerror("Erro",e)                                                      #cria janela de erro

    # Metódo para chamar a busca em profundidade
    def busca_profundidade(self):
        try:
            if self.arquivo_importado == False:
                raise Exception("Arquivo não importado")                                        #Gera exceção quando grafo não for importado
            visitados = list()                                                                  #Cria lista com a ordem de visitas
            self.graph.busca_profundidade(int(self.entryBuscaProfundidade.get()),visitados)     #Chama o algoritmo de busca em profundidade
            print(visitados)                                                                    #Exibe os resultados
            
        except Exception as e:
            messagebox.showerror("Erro", e)                                                     #Cria janela de erro
        
    # Metódo para chamar a busca em largura
    def busca_largura(self):
        try:
            if self.arquivo_importado == False:
                raise Exception("Arquivo não importado")                                        #Gera exceção quando grafo não for importado
            visitados = list()                                                                  #Gera lista com a ordem de visitas
            self.graph.busca_largura(int(self.entryBuscaLargura.get()),visitados)               #Chama o algoritmo de busca em largura
            print(visitados)                                                                    #Exibe os resultados
        except Exception as e:
            messagebox.showerror("Erro",e)                                                      #Cria janela de erro

    def busca_caminho(self):
        #try:
        #    if self.arquivo_importado == False:
        #        raise Exception("Arquivo não importado")
            
        #    visited = [False]*(self.graph.get_num_vertices())
            path = []
            resultado = self.graph.encontra_caminho(int(self.entryBuscaCaminho_1.get()),
                                        int(self.entryBuscaCaminho_2.get()),path)
            print(resultado)
                                        
        #    print("É conexo: ", self.graph.eh_conexo())
        #except Exception as e:
        #    messagebox.showerror("Erro",e)

janela  = Tk()
Tela(janela)
janela.mainloop()   

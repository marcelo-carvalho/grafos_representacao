# Algoritmos em grafos
# Engenharia de Computação Noturno
# Atividade 1 - Estrutura para representação de grafos 
# Aluno: Marcelo de Carvalho Pereira    Matricula: 687921
#
# A bibliiteca tkinter é fundamental para o funcionamento do programa
# gentileza se certificar de que a mesma incranta-se disponível 


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

    #metódo para visualização dos pares de arestas
    #def print_lista(self):
    #    for key in self.c_lista_adj.keys():
    #        print("Vértice", key, ": ",self.c_lista_adj[key])

    # Metódo para visualização dos resultados em prompt de comandos
    #def print_vertice(self, vertice):
    #    print("Sucessores", vertice, ":", self.c_lista_adj[vertice])
    #    print("Antecessores", vertice, ":", self.c_lista_adj_ant[vertice])
    #    print("Grau: ",len(self.c_lista_adj[vertice]))

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

#Classe para geração da janela 
class Tela:
    def __init__(self, master):
        self.mainTela = master
        self.mainTela.title("Grafos")
        self.mainTela.geometry('400x600')

        # Particição da Janela para diferentes agrupamentos de widgets
        self.frame_cima = Frame(self.mainTela).grid()
        self.frame_baixo = Frame(self.mainTela).grid()

        # Crio um título
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

janela  = Tk()
Tela(janela)
janela.mainloop()   

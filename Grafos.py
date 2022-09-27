from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


class Grafo:
    #construtor
    def __init__(self, num_vertices):
        self.c_num_vertices = num_vertices
        self.c_vertices = range(1,self.c_num_vertices)                              #determina dimensão da lista

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
    
    #Busca em Profundidade 
    def busca_profundidade(self,vertice,visitados):
        visitados.append(vertice)                                               #Inicia pilha com vértice escolhido pelo usuário
        for vizinho in self.c_lista_adj[vertice]:
            if vizinho not in visitados:
                self.busca_profundidade(vizinho,visitados)

    def DFS(self,vertice,ordem=[]):
        visited = [False for i in range(self.c_num_vertices)]
        stack = []
        stack.append(vertice)
        
        while(len(stack)):
            vertice = stack[-1]
            stack.pop()
            if(not visited[vertice]):
                ordem.append(vertice)
                visited[vertice] = True
            for node in self.c_lista_adj[vertice]:
                if (not visited[node]):
                    stack.append(node)


    #Busca em Largura Recursiva
    def busca_largura(self,vertice,visitados):
        fila = [vertice]                                                        #Inicia fila com vértice escolhido pelo usuário
        while fila:
            visitar = fila.pop(0)
            if visitar not in visitados:
                visitados.append(visitar)
                vizinhos = list(self.get_sucessores(visitar))
                fila.extend(vizinhos)
    
    #Busca em Largura Não Recursiva
    def BFS(self,vertice,ordem=[]):
        visited = [False] * (max(self.c_lista_adj)+1)
        queue = []
        queue.append(vertice)
        ordem.append(vertice)
        visited[vertice] = True
        
        while queue:
            vertice = queue.pop(0)
            ordem.append(vertice)
            for i in self.c_lista_adj[vertice]:
                if visited[i] == False:
                    queue.append(i)
                    visited[i] = True
    def encontrar_caminho_interativo(self,node1,node2,path=[]):
        
        if node1 == 0:
            return False
        if node2 == 0:
            return False
        if node1 not in self.c_lista_adj:
            return False
        if node2 not in self.c_lista_adj:
            return False

        visited = [False for i in range(self.c_num_vertices)]
        stack = []
        stack.append(node1)
        
        while(len(stack)):
            node1 = stack[-1]
            stack.pop()
            if(not visited[node1]):
                path.append(node1)
                visited[node1] = True
                if node1 == node2:
                    return path
            for node in self.c_lista_adj[node1]:
                if (not visited[node]):
                    stack.append(node)
        if len(path) + 2 == self.c_num_vertices:
            return False
    #Busca caminho entre dois vértices 
    def encontrar_caminho(self,node1,node2,path=[]):
        if node1 == 0:
            return False
        if node2 == 0:
            return False
        if node1 not in self.c_lista_adj:
            return False
        if node2 not in self.c_lista_adj:
            return False
        if len(path) + 2 == self.c_num_vertices:
            return False
        if(node2 in path):
            return path
        else:
            path.append(node1)
        for vizinho in self.c_lista_adj[node1]:
            if vizinho not in path:
                self.encontrar_caminho(vizinho,node2,path)
        return path
    
    def eh_conexo(self):
        dps =list()
        self.DFS(1,dps)
        if len(dps) < self.c_num_vertices-1:
            return False
        return True    
    
    def eh_ciclico(self,vertice,visitados=[]):
        fila = [vertice]                                                        #Inicia fila com vértice escolhido pelo usuário
        while fila:
            visitar = fila.pop(0)
            if visitar not in visitados:
                visitados.append(visitar)
                vizinhos = list(self.get_sucessores(visitar))
                fila.extend(vizinhos)
            else:
                return False
        return True

class Janela:
    def __init__(self, master):
        
        #widgets e variáveis de importação e grafo
        self.ImportacaoTitulo = Label(master,relief=GROOVE, text="Importação").place(x=5,y=10)
        self.ArquivoLabel = Label(master, text="Grafo: ").place(x=5,y=45)
        self.caminho_arquivo = StringVar()
        self.arquivo_importado = False
        self.LoadEntry = Entry(master,textvariable=self.caminho_arquivo,state="disabled")
        self.LoadEntry.place(x=55,y=45)
        self.LoadButton = Button(master,text="Load",command=self.carregar_arquivo).place(x=190, y=43)
        self.graph = None
        
        #widgets para atividade 1 
        self.Atividade1Titulo = Label(master,relief=GROOVE,text="Atividade 1").place(x=5,y=85)
        self.VerticeLabel = Label(master,text="Vértice: ").place(x=5,y=125)
        self.VerticeEntry = Entry(master)
        self.VerticeEntry.place(x=55,y=125)
        self.AntecessoresButton = Button(master,text="Buscar",command=self.buscarVertice).place(x=190,y=123)

        #widgets para atividade 2
        self.Atividade2Titulo = Label(master,relief=GROOVE, text="Atividade 2").place(x=5,y=165)
        self.VerticeBuscaLarguraLabel = Label(master,text='BFS: ').place(x=5,y=205)
        self.VerticeBuscaLarguraEntry = Entry(master)
        self.VerticeBuscaLarguraEntry.place(x=55,y=205)
        self.VerticeBuscaLarguraButton = Button(master,text="Buscar",command=self.busca_largura).place(x=190,y=200)
        self.VerticeBuscaProfundidadeLabel = Label(master,text='DFS: ').place(x=5,y=230)
        self.VerticeBuscaProfundidadeEntry = Entry(master)
        self.VerticeBuscaProfundidadeEntry.place(x=55,y=230)
        self.VerticeBuscaProfundidadeButton = Button(master,text="Buscar",command=self.busca_profundidade).place(x=190,y=230)
        
        self.TituloCaminhoLabel = Label(master,text="Busca Caminho").place(x=15,y=260)
        self.VerticeInicialLabel = Label(master,text="V Inicial: ").place(x=5,y=290)
        self.VerticeCaminhoInicialEntry = Entry(master)
        self.VerticeCaminhoInicialEntry.place(x=55,y=290)
        self.VerticeFinalLabel = Label(master, text="V Final: ").place(x=5,y=320)
        self.VerticeCaminhoFinalEntry = Entry(master)
        self.VerticeCaminhoFinalEntry.place(x=55,y=320)
        self.BuscarCaminhoButton = Button(master,text="Buscar Caminho",command=self.encontrar_caminho).place(x=190,y=300)
        
        self.TituloTestesLabel = Label(master,text="Testes").place(x=15,y=350)
        self.ConexoLabel = Label(master,text="Conexo? ").place(x=5,y=375)
        self.ConexoEntry = Entry(master,state="disabled")
        self.ConexoEntry.place(x=55,y=375)
        self.CiclicoLabel = Label(master,text="Cíclico? ").place(x=5,y=405)
        self.CiclicoEntry = Entry(master,state="disabled")
        self.CiclicoEntry.place(x=55,y=405)
        self.TestesButton = Button(master,text="Testar",command=self.testes).place(x=190,y=380)
    
    #Método para importação do arquivo
    def carregar_arquivo(self):
        self.caminho_arquivo = filedialog.askopenfilename()
        self.LoadEntry.config(state="normal")
        self.LoadEntry.delete(0,"end")
        self.LoadEntry.insert(0,self.caminho_arquivo)

        try:
            with open(self.caminho_arquivo,'r') as file_object:                                 #testa se o arquivo pode ser aberto
                texto = file_object.readlines()                                                 #faz a leitura do arquivo texto
                texto2 = [linha.rstrip('\n') for linha in texto]                                #separa os elementos por quebra de linha
                self.vertices = texto2[0].split()                                               #separa os elementos da primeira linha
                self.graph = Grafo(int(self.vertices[0])+1)                                     #gria o grafo de acordo com as entradas da primeira linha
                for i in range(int(self.vertices[1])+1):                                        #loop para população da lista 
                    if i > 0:                                                                   #ignra a primeira linha
                        aresta = texto[i].split()
                        self.graph.adiciona_aresta(int(aresta[0]),int(aresta[1]))
                messagebox.showinfo(title="Loading", message="Grafo carregado com sucesso.")    #mensagem de carregamento positivo
                self.arquivo_importado = True                                                   #flag indicando a confirmação do carregamento, libera pesquisa


        except:
            messagebox.showerror("Falha", "Ocorreu um erro durante a leitura do grafo.")        #exceção caso há erro no carregamento
            self.arquivo_importado = False                                                      #flag indicando falha no carregamento, bloqueia pesquisa
        

    #Método para  buscar antecessores e sucessores de um dado vértice 
    def buscarVertice(self):
        try:
            if(self.arquivo_importado == False):
                raise Exception("Arquivo não importado")                                        #se arquivo não importado gera exceção
            
            vertices_sucessores = self.graph.get_sucessores(int(self.VerticeEntry.get()))       #pega os elementos sucessores
            grau_sucessores = self.graph.get_grau_sucessores(int(self.VerticeEntry.get()))      #pega o grau de elementos sucessores
            vertices_antecessores = self.graph.get_antecessores(int(self.VerticeEntry.get()))   #pega os elementos antecessores
            grau_antecessores = self.graph.get_grau_antcessores(int(self.VerticeEntry.get()))   #pega o grau de elementos antecessores

            novaJanela = Tk()                                                                   #Cria uma janela para pesquisa solicitada
            novaJanela.geometry("400x250")
            nomeJanelaNova = "Graus e Adjacências vértice " + self.VerticeEntry.get()
            novaJanela.title(nomeJanelaNova)
            
            sucessores = Label(novaJanela,text="Vértices Sucessores")                           #Exibe os vértices sucessores
            sucessores.pack()
            resultado_sucessores = Label(novaJanela,wraplength=200,text=vertices_sucessores)    
            resultado_sucessores.pack()

            grauSucessores = Label(novaJanela,text="Grau de Sucessores")                        #Exibe o grau de vértices sucessores
            grauSucessores.pack()
            resultado_grauSucessores = Label(novaJanela,text=grau_sucessores)
            resultado_grauSucessores.pack()

            antecessores = Label(novaJanela,text="Vértices Antecessores")                       #Exibe os vértices antecessores
            antecessores.pack()
            resultado_antecessores = Label(novaJanela,wraplength=200,text=vertices_antecessores)
            resultado_antecessores.pack()

            grauAntecessores = Label(novaJanela,text="Grau de Antecessores")                    #Exibe o grau de vértices antecessores
            grauAntecessores.pack()
            resultado_grauAntecessores = Label(novaJanela,text=grau_antecessores)
            resultado_grauAntecessores.pack()
        
        except Exception as e:
            messagebox.showerror("Erro",e)  

    # Metódo para chamar a busca em profundidade
    def busca_profundidade(self):
        try:
            if self.arquivo_importado == False:
                raise Exception("Arquivo não importado")                                        #Gera exceção quando grafo não for importado

            visitados = list()                                                                 #Cria lista com a ordem de visitas
            self.graph.DFS(int(self.VerticeBuscaProfundidadeEntry.get()),visitados)            #Chama o algoritmo de busca em profundidade
            
            novaJanela = Tk()                                                                   #Cria uma janela para pesquisa solicitada
            novaJanela.geometry("400x250")
            nomeJanelaNova = "DFS vértice " + self.VerticeBuscaProfundidadeEntry.get()
            novaJanela.title(nomeJanelaNova)
            
            busca = Label(novaJanela,text="Vértices Visitados Interativo")                                 #Exibe os vértices visitados 
            busca.pack()
            resultado_busca = Label(novaJanela,wraplength=200,text=visitados)    
            resultado_busca.pack()
            
            print(visitados)                                                                    #Exibe os resultados
            
        except Exception as e:
            messagebox.showerror("Erro", e)                                                     #Cria janela de erro
    # Metódo para chamar a busca em largura
    def busca_largura(self):
        try:
            if self.arquivo_importado == False:
                raise Exception("Arquivo não importado")                                        #Gera exceção quando grafo não for importado
            
            visitados = list()                                                                  #Gera lista com a ordem de visitas
            self.graph.BFS(int(self.VerticeBuscaLarguraEntry.get()),visitados)                 #Chama o algoritmo de busca em largura
            
            novaJanela = Tk()                                                                   #Cria uma janela para pesquisa solicitada
            novaJanela.geometry("400x250")
            nomeJanelaNova = "BFS vértice " + self.VerticeBuscaLarguraEntry.get()
            novaJanela.title(nomeJanelaNova)
            
            busca = Label(novaJanela,text="Vértices Visitados")                                 #Exibe os vértices visitados 
            busca.pack()
            resultado_busca = Label(novaJanela,wraplength=200,text=visitados)    
            resultado_busca.pack()

            print(visitados)                                                                    #Exibe os resultados
        except Exception as e:
            messagebox.showerror("Erro",e)                                                      #Cria janela de erro
    
    def encontrar_caminho(self):
        try:
            resultados = []
            self.graph.encontrar_caminho_interativo(int(self.VerticeCaminhoInicialEntry.get()),
                                         int(self.VerticeCaminhoFinalEntry.get()),
                                         resultados)
            if resultados:
                novaJanela = Tk()                                                                   #Cria uma janela para pesquisa solicitada
                novaJanela.geometry("400x250")
                nomeJanelaNova = "Caminho: " + self.VerticeCaminhoInicialEntry.get() +\
                                " -> " + self.VerticeCaminhoFinalEntry.get()
                novaJanela.title(nomeJanelaNova)
                
                caminho = Label(novaJanela,text="Vértices Visitados")                                 #Exibe os vértices visitados 
                caminho.pack()
                resultado_busca = Label(novaJanela,wraplength=200,text=resultados)    
                resultado_busca.pack()

                print(resultados)
            else:
                raise Exception("Não existe caminho")
        except Exception as e:
            messagebox.showerror("Erro",e)
    
    def testes(self):
        
        try:
            if(self.arquivo_importado == False):
                raise Exception("Arquivo não importado")     
            
            conexo = self.graph.eh_conexo()
            ciclico = self.graph.eh_ciclico(1)
            if conexo:
                self.ConexoEntry.config(state="normal")
                self.ConexoEntry.delete(0,"end")
                self.ConexoEntry.insert(0,"Sim")
            else:
                self.ConexoEntry.configse(self,state="normal")
                self.ConexoEntry.delete(0,"end")
                self.ConexoEntry.insert(0,"Não")
            if ciclico:
                self.CiclicoEntry.config(state="normal")
                self.CiclicoEntry.delete(0,"end")
                self.CiclicoEntry.insert(0,"Sim")
            else:
                self.CiclicoEntry.config(state="normal")
                self.CiclicoEntry.delete(0,"end")
                self.CiclicoEntry.insert(0,"Não")

        except Exception as e:
            messagebox.showerror("Erro",e)        
        

root = Tk()
root.title("Grafos")
root.geometry('400x450+250+200')
Janela(root)
root.mainloop()
import tkinter as tk
from tkinter import filedialog
import math


class Graph:
    def __init__(self, vertices=0):
        self.vertices = vertices
        self.adj_list = [[] for _ in range(vertices)]

    def add_edge(self, u, v):
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)

    def remove_edge(self, u, v):
        self.adj_list[u].remove(v)
        self.adj_list[v].remove(u)

    #def is_connected(self):
        #if self.vertices == 0:
            #return True
        #visited = [False] * self.vertices
        #self.dfs(0, visited)
        #return all(visited)

    #def dfs(self, v, visited):
        #visited[v] = False
        #for neighbor in self.adj_list[v]:
            #if not visited[neighbor]:
                #self.dfs(neighbor, visited)


    def dfs(self, start, visited):
        visited[start] = True

        for neighbor in self.adj_list[start]:
            if not visited[neighbor]:
                self.dfs(neighbor, visited)
                
    def is_connected(self):
        visited = [False] * self.vertices
        self.dfs(0, visited)

        return all(visited)
                  
    def remove_vertex(self, v):
        if v < 0 or v >= self.vertices:
            raise ValueError("Invalid vertex index")

        for neighbor in self.adj_list[v]:
            self.adj_list[neighbor-1].remove(v)
        self.adj_list[v] = []

        self.vertices -= 1

        for u in range(self.vertices):
            for i in range(len(self.adj_list[u])):
                if self.adj_list[u][i] > v:
                    self.adj_list[u][i] -= 1


class NetworkGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("网络通路管理")
        self.window.geometry("800x500")

        self.graph = None

        self.vertices = 0

        # 菜单栏
        menu_bar = tk.Menu(self.window)
        self.window.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="新建", command=self.new_network)
        file_menu.add_command(label="打开", command=self.open_network)
        file_menu.add_command(label="保存", command=self.save_network)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="编辑", menu=edit_menu)
        edit_menu.add_command(label="添加节点", command=self.add_vertex)
        edit_menu.add_command(label="删除节点", command=self.remove_vertex)
        edit_menu.add_command(label="添加连接", command=self.add_edge)
        edit_menu.add_command(label="删除连接", command=self.remove_edge)

        # 信息栏
        self.info_label = tk.Label(self.window, text="请选择操作...")
        self.info_label.pack(side=tk.TOP, fill=tk.X)

        # 画布
        self.canvas = tk.Canvas(self.window, width=600, height=400, bg="white")
        self.canvas.pack(side=tk.TOP, padx=20, pady=20)



        # 运行按钮
        #run_button = tk.Button(self.window, text="运行", command=self.run)
        #run_button.pack(side=tk.BOTTOM)


    def new_network(self):
        self.vertices = 0
        self.graph = Graph(self.vertices)
        self.draw_network()
        self.info_label.config(text="成功创建新网络！")

    def open_network(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as f:
                lines = f.readlines()
                self.vertices = int(lines[0])
                self.graph = Graph(self.vertices)
                for line in lines[1:]:
                    u, v = map(int, line.split())
                    self.graph.add_edge(u, v)
                self.draw_network()
                self.info_label.config(text="成功打开网络")

    def save_network(self):
        if not self.graph:
            self.info_label.config(text="当前没有网络可以保存！")
            return
        file_path = filedialog.asksaveasfilename()
        if file_path:
            with open(file_path, "w") as f:
                f.write(str(self.vertices) + "\n")
                for u in range(self.vertices):
                    for v in self.graph.adj_list[u]:
                        if u < v:
                            f.write(str(u) + " " + str(v) + "\n")
            self.info_label.config(text="成功保存网络！")

    #def remove_vertex(self):
        #if self.vertices == 0:
            #self.info_label.config(text="当前没有节点可以删除！")
            #return
        #v = int(input("请输入要删除的节点编号："))
        #if v < 0 or v >= self.vertices:
            #self.info_label.config(text="节点编号不合法，请重新输入！")
            #return
        #self.graph.remove_vertex(v)
        #self.draw_network()
        #self.info_label.config(text="成功删除节点！")



    def add_vertex(self):
        self.vertices += 1
        self.graph.adj_list.append([])
        self.draw_network()
        self.info_label.config(text="成功添加节点！")

    def add_edge(self):
        if self.vertices < 2:
            self.info_label.config(text="当前没有足够的节点可以连接！")
            return
        u, v = map(int, input("请输入两个节点的编号（用空格分隔）：").split())
        if u < 0 or u >= self.vertices or v < 0 or v >= self.vertices or u == v:
            self.info_label.config(text="节点编号不合法，请重新输入！")
            return
        if v not in self.graph.adj_list[u]:
            self.graph.add_edge(u, v)
            self.draw_network()
            if self.graph.is_connected():
                self.info_label.config(text="成功添加连接！")
            else:
                self.info_label.config(text="添加连接后网络不连通，请重新操作！")
        else:
            self.info_label.config(text="连接已存在，请重新输入！")

    def remove_edge(self):
        if self.vertices < 2:
            self.info_label.config(text="当前没有足够的节点可以删除连接！")
            return
        u, v = map(int, input("请输入两个节点的编号（用空格分隔）：").split())
        if u < 0 or u >= self.vertices or v < 0 or v >= self.vertices or u == v:
            self.info_label.config(text="节点编号不合法，请重新输入！")
            return
        if v in self.graph.adj_list[u]:
            self.graph.remove_edge(u, v)
            self.draw_network()
            if self.graph.is_connected():
                self.info_label.config(text="成功删除连接！")
            else:
                self.info_label.config(text="删除连接后网络不连通，请重新操作！")
        else:
            self.info_label.config(text="连接不存在，请重新输入！")

    def draw_network(self):
        self.canvas.delete("all")
        if not self.graph:
            return
        node_size = 30
        node_padding = 50
        cx, cy = self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2
        radius = min(cx, cy) - node_padding
        node_positions = [(cx + radius * math.cos(2 * math.pi * i / self.vertices),
                           cy + radius * math.sin(2 * math.pi * i / self.vertices))
                          for i in range(self.vertices)]
        for u in range(self.vertices):
            for v in self.graph.adj_list[u]:
                if u < v:
                    self.canvas.create_line(node_positions[u], node_positions[v])
        for i, pos in enumerate(node_positions):
            self.canvas.create_oval(pos[0] - node_size // 2, pos[1] - node_size // 2,
                                    pos[0] + node_size // 2, pos[1] + node_size // 2,
                                    fill="white")
            self.canvas.create_text(pos[0], pos[1], text=str(i))

    def remove_vertex(self):
        if self.vertices < 1:
            self.info_label.config(text="当前没有足够的节点可以删除！")
            return
        u = int(input("请输入要删除的节点的编号："))
        if u < 0 or u >= self.vertices:
            self.info_label.config(text="节点编号不合法，请重新输入！")
            return
        self.graph.remove_vertex(u)
        self.vertices -= 1
        self.draw_network()
        if self.graph.is_connected():
            self.info_label.config(text="成功删除节点！")
        else:
            self.info_label.config(text="删除节点后网络不连通，请重新操作！")

    def load_network(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as f:
                self.vertices = int(f.readline())
                self.graph = Graph(self.vertices)
                for line in f.readlines():
                    u, v = map(int, line.split())
                    self.graph.add_edge(u, v)
            self.draw_network()
            if self.graph.is_connected():
                self.info_label.config(text="成功加载网络！")
            else:
                self.info_label.config(text="加载网络后网络不连通，请重新操作！")


    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    gui = NetworkGUI()
    gui.run()

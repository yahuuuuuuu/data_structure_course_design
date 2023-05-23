from queue import Queue
import tkinter as tk
from tkinter import filedialog
import math


class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.adj_matrix = [[0] * self.V for _ in range(self.V)]

    def add_edge(self, u, v):
        self.adj_matrix[u][v] = 1
        self.adj_matrix[v][u] = 1

    def remove_edge(self,u,v):
        self.adj_matrix[u][v] = 0
        self.adj_matrix[v][u] = 0

    def bfs(self, s):
        # 初始化所有顶点为未访问状态
        visited = [False] * self.V
        # 将起始顶点标记为已访问，并将其加入队列中
        visited[s] = True
        queue = Queue()
        queue.put(s)

        # 循环直到队列为空
        while not queue.empty():
            # 取出队列中的下一个顶点
            u = queue.get()
            # 遍历与当前顶点相邻的顶点
            for v in range(self.V):
                # 如果相邻顶点未被访问，则标记为已访问，并将其加入队列中
                if self.adj_matrix[u][v] == 1 and not visited[v]:
                    visited[v] = True
                    queue.put(v)

        # 判断所有顶点是否都被访问过
        for i in range(self.V):
            if not visited[i]:
                return False
        return True




class NetworkGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("网络通路管理")
        self.window.geometry("800x500")

        self.graph = None
        self.text = ""
        self.vertices = 0

        # 菜单栏
        menu_bar = tk.Menu(self.window)
        self.window.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="新建", command=self.new_network)
        file_menu.add_command(label="打开", command=self.load_network)
        file_menu.add_command(label="保存", command=self.save_network)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="编辑", menu=edit_menu)
        edit_menu.add_command(label="添加连接", command=self.add_edge)
        edit_menu.add_command(label="删除连接", command=self.remove_edge)

        # 信息栏
        self.info_label = tk.Label(self.window, text="请选择操作...")
        self.info_label.pack(side=tk.TOP, fill=tk.X)

        # 画布
        self.canvas = tk.Canvas(self.window, width=600, height=400, bg="white")
        self.canvas.pack(side=tk.TOP, padx=20, pady=20)

        # 输入框
        #self.label = tk.Label(self.window, text='')
        #self.label.pack(side=tk.TOP, fill=tk.X)
        #self.textbox = tk.Entry(self.window)
        #self.textbox.bind("<Return>", self.on_enter)
        #self.textbox.pack(side=tk.TOP)



        # 运行按钮
        #run_button = tk.Button(self.window, text="运行", command=self.run)
        #run_button.pack(side=tk.BOTTOM)

    def on_enter(self,event):
        self.text = '0'
        self.text = self.textbox.get()
        print(self.text)
        self.textbox.delete(0, tk.END)

    def new_network(self):
        #self.label.config(text="图的节点数为;")

        #print(self.text)
        self.vertices = int(input('图的节点数为:'))

        #print(self.vertices)
        self.graph = Graph(vertices=self.vertices)
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
        if self.graph.bfs(0):
            self.info_label.config(text="成功加载网络！")
        else:
            self.info_label.config(text="加载网络后网络不连通，请重新操作！")

    def save_network(self):
        if not self.graph:
            self.info_label.config(text="当前没有网络可以保存！")
            return
        file_path = filedialog.asksaveasfilename()
        if file_path:
            with open(file_path, "w") as f:
                f.write(str(self.vertices) + "\n")
                for u in range(self.vertices):
                    for v in range(self.vertices):
                        if self.graph.adj_matrix[u][v] == 1 and u < v:
                            f.write(str(u) + " " + str(v) + "\n")
        self.info_label.config(text="成功保存网络！")

    def add_edge(self):
        #self.label.config(text='请输入两个节点的编号（用空格分隔）：')
        #self.text = self.textbox.get()
        #self.u = int(self.text.split(' ')[0])
        #self.v = int(self.text.split(' ')[1])
        #self.graph.add_edge(self.u, self.v)
        #self.textbox.delete(0,tk.END)

        if self.vertices < 2:
            self.info_label.config(text="当前没有足够的节点可以连接！")
            return
        u, v = map(int, input("请输入两个节点的编号（用空格分隔）：").split())
        if u < 0 or u >= self.vertices or v < 0 or v >= self.vertices or u == v:
            self.info_label.config(text="节点编号不合法，请重新输入！")
            return
        if self.graph.adj_matrix[u][v] == 0:
            self.graph.add_edge(u, v)
            self.draw_network()
            if self.graph.bfs(0):
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
        if self.graph.adj_matrix[u][v] == 1:
            self.graph.remove_edge(u, v)
            self.draw_network()
            if self.graph.bfs(0):
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
            for v in range(self.vertices):
                if self.graph.adj_matrix[u][v]:
                    if u < v:
                        self.canvas.create_line(node_positions[u], node_positions[v])

        for i, pos in enumerate(node_positions):
            self.canvas.create_oval(pos[0] - node_size // 2, pos[1] - node_size // 2,
                                    pos[0] + node_size // 2, pos[1] + node_size // 2,
                                    fill="white")
            self.canvas.create_text(pos[0], pos[1], text=str(i))

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    gui = NetworkGUI()
    gui.run()

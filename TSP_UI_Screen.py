import tkinter as tk
from tkinter import messagebox
import math

class ScreenUI:
    def __init__(self):
        self.input_text = None

        # Configuração da janela principal
        self.jf = tk.Tk()
        self.jf.title("Drone++")
        self.jf.geometry("1280x720")
        self.jf.protocol("WM_DELETE_WINDOW", self.jf.destroy)

        # Botões na tela inicial
        jb1 = tk.Button(self.jf, text="SET INPUT", command=self.input_ui, font=("Impact", 40))
        jb2 = tk.Button(self.jf, text="GUIDE", command=self.show_guide, font=("Impact", 40))

        jb1.place(x=452, y=249, width=375, height=91)
        jb2.place(x=452, y=380, width=375, height=91)

        self.jf.mainloop()

    def input_ui(self):
        # Janela para entrada de texto
        jf2 = tk.Toplevel(self.jf)
        jf2.title("Drone++")
        jf2.geometry("1280x720")

        # Caixa de entrada de texto e botão
        self.input_text = tk.Entry(jf2, font=("Impact", 28))
        jb4 = tk.Button(jf2, text="CLICK HERE", command=self.output_message, font=("Impact", 40))

        self.input_text.place(x=452, y=249, width=375, height=91)
        jb4.place(x=452, y=380, width=375, height=91)

    def dist(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def output_message(self):
        str_input = self.input_text.get()
        args = str_input.split()
        n = int(args[0])
        x, y = [], []

        for i in range(1, 2 * n + 1, 2):
            x.append(float(args[i]))
            y.append(float(args[i + 1]))

        dp = [[0] * (1 << n) for _ in range(n)]
        prv = [[-1] * (1 << n) for _ in range(n)]

        for i in range(n):
            dp[i][(1 << i)] = self.dist(0, 0, x[i], y[i])
            prv[i][(1 << i)] = -1

        for mask in range(1, (1 << n)):
            for i in range(n):
                for j in range(n):
                    if i == j:
                        continue

                    if (mask >> i) & 1 == 1 and (mask >> j) & 1 == 0:
                        if dp[j][mask | (1 << j)] == 0 or dp[j][mask | (1 << j)] > dp[i][mask] + self.dist(
                                x[i], y[i], x[j], y[j]):
                            dp[j][mask | (1 << j)] = dp[i][mask] + self.dist(x[i], y[i], x[j], y[j])
                            prv[j][mask | (1 << j)] = i

        tmp = float('inf')
        id = -1

        for i in range(n):
            if dp[i][(1 << n) - 1] + self.dist(0, 0, x[i], y[i]) < tmp:
                tmp = dp[i][(1 << n) - 1] + self.dist(0, 0, x[i], y[i])
                id = i

        path = []
        mask = (1 << n) - 1
        path.append(-1)

        while id != -1:
            path.append(id)
            nid = prv[id][mask]
            mask ^= (1 << id)
            id = nid

        path.append(-1)

        output1 = f"{tmp} is the total distance."
        output2 = "The order of the points:\n"

        for i in range(len(path)):
            if path[i] == -1:
                output2 += " (0,0)\n"
            else:
                output2 += f" ({x[path[i]]},{y[path[i]]})\n"

        messagebox.showinfo("Output", output1)
        messagebox.showinfo("Output", output2)

    def show_guide(self):
        messagebox.showinfo("Guide", "Please go to 'Set Input' and enter the coordinates that the drone should reach.\nThen, our app will give you the shortest path passing through all the points.")


# Instanciando a classe e iniciando o programa
ui = ScreenUI()
import tkinter as tk
from tkinter import filedialog
import re
import networkx as nx
import matplotlib.pyplot as plt
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from itertools import cycle
from collections import Counter

G = None
pos = {}  # 布局坐标缓存
stop_walk = False
walk_thread = None
visited_nodes = []
visited_edges = []


def clean_text(text):
    text = re.sub(r'[^A-Za-z\s]', ' ', text)
    text = text.lower()
    return text.split()


def build_graph(words):
    Graph = nx.DiGraph()
    for i in range(len(words) - 1):
        a, b = words[i], words[i + 1]
        if Graph.has_edge(a, b):
            Graph[a][b]['weight'] += 1
        else:
            Graph.add_edge(a, b, weight=1)
    return Graph


def draw_graph(Graph, local_canvas_frame, highlight_edges_list=None):
    global pos
    fig, ax = plt.subplots(figsize=(10, 8))
    for widget in local_canvas_frame.winfo_children():
        widget.destroy()
    # try:
    #     pos = nx.nx_agraph.graphviz_layout(Graph, prog='dot')
    # except (ImportError, ValueError, nx.NetworkXException):
    #     pos = nx.kamada_kawai_layout(Graph)
    # try:
    #     pos = nx.nx_agraph.graphviz_layout(Graph, prog='dot')
    # except:
    #     pos = nx.kamada_kawai_layout(Graph)
    pos = nx.kamada_kawai_layout(Graph)
    # try:
    #     # 尝试使用 Graphviz 的 dot 布局
    #     pos = nx.nx_agraph.graphviz_layout(Graph, prog='dot')
    # except (ImportError, nx.NetworkXException) as e:
    #     print(f"Graphviz 布局失败，使用备用布局：{e}")
    #     # 备用布局：Kamada-Kawai
    #     pos = nx.kamada_kawai_layout(Graph)

    nx.draw(Graph, pos, ax=ax, with_labels=True, node_color='lightblue',
            node_size=600, font_size=10, arrows=True, arrowsize=20,
            connectionstyle='arc3,rad=0.1')

    edge_labels = nx.get_edge_attributes(Graph, 'weight')
    nx.draw_networkx_edge_labels(
        Graph,
        pos,
        edge_labels=edge_labels,
        ax=ax,
        font_size=8
    )

    if highlight_edges_list:
        colors = cycle([
            'red',
            'green',
            'purple',
            'orange',
            'brown',
            'magenta'
        ])

        for path_edges in highlight_edges_list:
            color = next(colors)
            nx.draw_networkx_edges(Graph, pos, edgelist=path_edges,
                                   edge_color=color,
                                   width=2.5,
                                   ax=ax,
                                   connectionstyle='arc3,rad=0.1')

    canvas = FigureCanvasTkAgg(fig, master=local_canvas_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()


def open_file():
    global G
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read().replace('\n', ' ')
            words = clean_text(text)
            G = build_graph(words)
            draw_graph(G, canvas_frame)
            result_var.set("图构建完成。可以查找桥接词、生成新文本或查询最短路径。")


def find_bridge_words():
    word1 = entry_word1.get().lower().strip()
    word2 = entry_word2.get().lower().strip()
    if G is None:
        result_var.set("请先加载文本文件并生成图！")
        return
    if word1 not in G or word2 not in G:
        result_var.set(f"No {word1} or {word2} in the graph!")
        return

    bridge_words = [w3 for w3 in G.successors(word1) if G.has_edge(w3, word2)]
    if not bridge_words:
        result_var.set(f"No bridge words from {word1} to {word2}!")
    else:
        if len(bridge_words) == 1:
            result = (
                f"The bridge word from {word1} to {word2} "
                f"is: {bridge_words[0]}."
            )

        else:
            formatted = (
                ", ".join(bridge_words[:-1])
                + f", and {bridge_words[-1]}"
            )
            result = (
                f"The bridge words from {word1} to {word2} are: {formatted}."
            )
        result_var.set(result)


def generate_new_text():
    if G is None:
        result_var.set("请先加载文本文件并生成图！")
        return
    text = entry_new_sentence.get().strip()
    words = clean_text(text)
    if len(words) < 2:
        result_var.set("请输入至少两个单词！")
        return

    new_words = []
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        new_words.append(w1)
        if w1 in G and w2 in G:
            bridges = [w3 for w3 in G.successors(w1) if G.has_edge(w3, w2)]
            if bridges:
                bridge = random.choice(bridges)
                new_words.append(bridge)
    new_words.append(words[-1])
    result = " ".join(new_words)
    result_var.set("生成新文本：\n" + result)


def find_shortest_path():
    word1 = entry_word1.get().lower().strip()
    word2 = entry_word2.get().lower().strip()
    if G is None:
        result_var.set("请先加载文本文件并生成图！")
        return
    if not word1:
        result_var.set("请输入至少一个单词！")
        return

    if word1 not in G:
        result_var.set(f"单词 '{word1}' 不在图中！")
        return

    if word2 and word2 not in G:
        result_var.set(f"单词 '{word2}' 不在图中！")
        return

    if word2:
        try:
            all_paths = list(nx.all_shortest_paths(G,
                                                   source=word1,
                                                   target=word2,
                                                   weight='weight'))
            result_lines = []
            highlight_paths = []
            for path in all_paths:
                weight = sum(
                    G[path[i]][path[i + 1]]['weight']
                    for i in range(len(path) - 1))
                result_lines.append(" -> ".join(path) + f"（路径长度: {weight}）")
                edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
                highlight_paths.append(edges)

            draw_graph(G, canvas_frame, highlight_edges_list=highlight_paths)
            result = f"{word1} 到 {word2} 的所有最短路径：\n" + "\n".join(result_lines)
            result_var.set(result)
        except nx.NetworkXNoPath:
            result_var.set(f"{word1} 到 {word2} 不可达。")
    else:
        paths = nx.single_source_dijkstra_path(G, word1, weight='weight')
        lengths = nx.single_source_dijkstra_path_length(G,
                                                        word1,
                                                        weight='weight')
        result_lines = []
        for target, path in paths.items():
            if target == word1:
                continue
            line = (
                f"{word1} -> {target}：路径 = {' -> '.join(path)}, "
                f"长度 = {lengths[target]}"
            )

            result_lines.append(line)
        result_var.set("\n".join(result_lines[:30]))
        draw_graph(G, canvas_frame)


def calculate_pagerank(Graph,
                       damping_factor,
                       max_iter=100,
                       tol=1e-6,
                       word_list=None):
    N = len(Graph)
    if N == 0:
        return {}

    # 计算词频并归一化
    if word_list:
        freq = Counter(word_list)
        total = sum(freq[node] for node in Graph if node in freq)
        pr = {node: freq[node] / total
              if node in freq else 0 for node in Graph}
    else:
        pr = {node: 1 / N for node in Graph}

    nodes = list(Graph.nodes())

    for _ in range(max_iter):
        new_pr = {}
        dangling_sum = sum(
            pr[node]
            for node in nodes if Graph.out_degree(node) == 0)

        for node in nodes:
            rank = (1 - damping_factor) / N
            rank += damping_factor * dangling_sum / N

            for pred in Graph.predecessors(node):
                if Graph.out_degree(pred) > 0:
                    rank += damping_factor * pr[pred] / Graph.out_degree(pred)
            new_pr[node] = rank

        diff = sum(abs(new_pr[node] - pr[node]) for node in nodes)
        pr = new_pr
        if diff < tol:
            break

    return pr


def calculate_and_display_pagerank():
    if G is None:
        result_var.set("请先加载文本文件并生成图！")
        return

    damping_factor = float(entry_damping.get())
    pagerank = calculate_pagerank(G, damping_factor)
    result = "PageRank值：\n"
    for node, rank in pagerank.items():
        result += f"{node}: {rank:.4f}\n"

    result_var.set(result)


def random_walk():
    global stop_walk, visited_nodes, visited_edges
    if G is None:
        result_var.set("请先加载文本文件并生成图！")
        return

    visited_nodes = []
    visited_edges = []

    current_node = random.choice(list(G.nodes()))
    visited_nodes.append(current_node)

    stop_walk = False

    def walk_step():
        nonlocal current_node
        if stop_walk:
            save_walk_results()
            return

        neighbors = list(G.successors(current_node))
        if not neighbors:
            save_walk_results()
            return
        next_node = random.choice(neighbors)
        edge = (current_node, next_node)

        if edge in visited_edges:
            save_walk_results()
            return

        visited_edges.append(edge)
        visited_nodes.append(next_node)

        current_node = next_node
        result_var.set("随机游走节点：\n" + " -> ".join(visited_nodes))
        root.after(500, walk_step)

    walk_step()


def stop_random_walk():
    global stop_walk
    stop_walk = True
    result_var.set("随机游走已停止。")


def save_walk_results():
    with open("random_walk_results.txt", "w", encoding="utf-8") as f:
        f.write("经过的节点：\n")
        f.write(" -> ".join(visited_nodes) + "\n")
        f.write("经过的边：\n")
        for edge in visited_edges:
            f.write(f"{edge}\n")
    result_var.set("随机游走结果已保存到文件：random_walk_results.txt")


# GUI界面
root = tk.Tk()
root.title("文本图分析器")
root.geometry("1024x960")

btn = tk.Button(root, text="选择文本文件", command=open_file, font=('Arial', 14))
btn.pack(pady=10)

input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame,
         text="Word 1:",
         font=('Arial', 12)).grid(row=0, column=0, padx=5)
entry_word1 = tk.Entry(input_frame, width=15, font=('Arial', 12))
entry_word1.grid(row=0, column=1, padx=5)

tk.Label(input_frame,
         text="Word 2:",
         font=('Arial', 12)).grid(row=0, column=2, padx=5)
entry_word2 = tk.Entry(input_frame, width=15, font=('Arial', 12))
entry_word2.grid(row=0, column=3, padx=5)

btn_find = tk.Button(input_frame,
                     text="查找桥接词",
                     command=find_bridge_words,
                     font=('Arial', 12))
btn_find.grid(row=0, column=4, padx=5)

btn_path = tk.Button(input_frame,
                     text="最短路径查询",
                     command=find_shortest_path,
                     font=('Arial', 12))
btn_path.grid(row=0, column=5, padx=5)

input_frame_pagerank = tk.Frame(root)
input_frame_pagerank.pack(pady=10)

tk.Label(input_frame_pagerank,
         text="阻尼因子(damping):",
         font=('Arial', 12)).grid(row=0, column=0, padx=5)
entry_damping = tk.Entry(input_frame_pagerank, width=10, font=('Arial', 12))
entry_damping.grid(row=0, column=1, padx=5)
entry_damping.insert(0, "0.85")

btn_pagerank = tk.Button(input_frame_pagerank,
                         text="计算PageRank",
                         command=calculate_and_display_pagerank,
                         font=('Arial', 12))
btn_pagerank.grid(row=0, column=2, padx=5)

btn_walk = tk.Button(root,
                     text="开始随机游走",
                     command=random_walk,
                     font=('Arial', 12))
btn_walk.pack(pady=10)

btn_stop_walk = tk.Button(root,
                          text="停止随机游走",
                          command=stop_random_walk,
                          font=('Arial', 12))
btn_stop_walk.pack(pady=10)

sentence_frame = tk.Frame(root)
sentence_frame.pack(pady=10)

tk.Label(sentence_frame,
         text="输入新文本：",
         font=('Arial', 12)).pack(side=tk.LEFT, padx=5)
entry_new_sentence = tk.Entry(sentence_frame, width=60, font=('Arial', 12))
entry_new_sentence.pack(side=tk.LEFT, padx=5)

btn_generate = tk.Button(sentence_frame,
                         text="生成新文本",
                         command=generate_new_text,
                         font=('Arial', 12))
btn_generate.pack(side=tk.LEFT, padx=10)

result_var = tk.StringVar()
result_label = tk.Label(root,
                        textvariable=result_var,
                        wraplength=960,
                        justify="left",
                        font=('Arial', 12),
                        fg="blue")
result_label.pack(pady=10)

canvas_frame = tk.Frame(root)
canvas_frame.pack(pady=10)

root.mainloop()

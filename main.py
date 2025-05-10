import tkinter as tk
from tkinter import filedialog
import re
import networkx as nx
import matplotlib.pyplot as plt
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

G = None
pos = {}  # 布局坐标缓存
stop_walk = False  # 停止标志位
walk_thread = None  # 用于存储随机游走线程
visited_nodes = []  # 记录遍历的节点
visited_edges = []  # 记录遍历的边


def clean_text(text):
    # 输入一个文本文件，其中包含用英文书写的文本数据；
    #  文本分为多行，你的程序应默认将换行 / 回车符当作空格；
    #  文本中的任何标点符号，也应当作空格处理；
    #  文本中的非字母(A - Z和a - z之外)
    # 字符应被忽略。

    text = re.sub(r'[^A-Za-z\s]', ' ', text)
    text = text.lower()
    return text.split()


def build_graph(words):
    G = nx.DiGraph()
    for i in range(len(words) - 1):
        a, b = words[i], words[i + 1]
        if G.has_edge(a, b):
            G[a][b]['weight'] += 1
        else:
            G.add_edge(a, b, weight=1)
    return G


def draw_graph(G, canvas_frame, highlight_edges=None):
    global pos
    fig, ax = plt.subplots(figsize=(10, 8))
    for widget in canvas_frame.winfo_children():
        widget.destroy()
    try:
        pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
    except:
        pos = nx.kamada_kawai_layout(G)

    normal_edges = list(G.edges())
    edge_colors = ['red' if highlight_edges and (u, v) in highlight_edges else 'blue' for u, v in normal_edges]
    edge_widths = [2.5 if highlight_edges and (u, v) in highlight_edges else 1 for u, v in normal_edges]

    nx.draw(G, pos, ax=ax, with_labels=True, node_color='lightblue', node_size=600,
            font_size=10, arrows=True, arrowsize=20, edge_color=edge_colors,
            width=edge_widths, connectionstyle='arc3,rad=0.1')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_size=8)

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
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
            result = f"The bridge word from {word1} to {word2} is: {bridge_words[0]}."
        else:
            formatted = ", ".join(bridge_words[:-1]) + f", and {bridge_words[-1]}"
            result = f"The bridge words from {word1} to {word2} are: {formatted}."
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
            path = nx.shortest_path(G, source=word1, target=word2, weight='weight')
            weight = sum(G[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1))
            result = f"{word1} 到 {word2} 的最短路径为：\n" + " -> ".join(path) + f"\n路径长度：{weight}"
            highlight = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            draw_graph(G, canvas_frame, highlight_edges=highlight)
            result_var.set(result)
        except nx.NetworkXNoPath:
            result_var.set(f"{word1} 到 {word2} 不可达。")
    else:
        paths = nx.single_source_dijkstra_path(G, word1, weight='weight')
        lengths = nx.single_source_dijkstra_path_length(G, word1, weight='weight')
        result_lines = []
        for target, path in paths.items():
            if target == word1:
                continue
            line = f"{word1} -> {target}：路径 = {' -> '.join(path)}, 长度 = {lengths[target]}"
            result_lines.append(line)
        result_var.set("\n".join(result_lines[:30]))  # 限制显示30项以防太长
        draw_graph(G, canvas_frame)


def calculate_pagerank(G, damping_factor):
    N = len(G)
    pagerank = {node: 1 / N for node in G}
    for _ in range(30):  # Iterations
        new_pagerank = {}
        for node in G:
            rank_sum = sum(pagerank[neighbor] / len(list(G.neighbors(neighbor))) for neighbor in G.predecessors(node))
            new_pagerank[node] = (1 - damping_factor) / N + damping_factor * rank_sum
        pagerank = new_pagerank
    return pagerank


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
    global stop_walk, walk_thread, visited_nodes, visited_edges
    if G is None:
        result_var.set("请先加载文本文件并生成图！")
        return

    # 初始化
    visited_nodes = []
    visited_edges = []

    # 从随机节点开始
    current_node = random.choice(list(G.nodes()))
    visited_nodes.append(current_node)

    stop_walk = False  # Reset stop_walk flag each time we start a new walk

    def walk_step():
        nonlocal current_node
        if stop_walk:
            save_walk_results()  # 保存结果
            return

        neighbors = list(G.successors(current_node))
        if not neighbors:  # 没有出边，停止
            save_walk_results()
            return
        next_node = random.choice(neighbors)
        edge = (current_node, next_node)

        # 如果这条边已经遍历过，停止
        if edge in visited_edges:
            save_walk_results()
            return

        # 记录节点和边
        visited_edges.append(edge)
        visited_nodes.append(next_node)

        # 更新当前节点
        current_node = next_node

        # 更新显示
        result_var.set(f"随机游走节点：\n" + " -> ".join(visited_nodes))
        root.after(500, walk_step)  # 每500ms走一步

    walk_step()


def stop_random_walk():
    global stop_walk
    stop_walk = True
    result_var.set("随机游走已停止。")


def save_walk_results():
    # 保存到文件
    with open("random_walk_results.txt", "w", encoding="utf-8") as f:
        f.write("经过的节点：\n")
        f.write(" -> ".join(visited_nodes) + "\n")
        f.write("经过的边：\n")
        for edge in visited_edges:
            f.write(f"{edge}\n")
    result_var.set(f"随机游走结果已保存到文件：random_walk_results.txt")


# GUI界面
root = tk.Tk()
root.title("文本图分析器")
root.geometry("1024x960")

btn = tk.Button(root, text="选择文本文件", command=open_file, font=('Arial', 14))
btn.pack(pady=10)

# 桥接词和路径查询区域
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Word 1:", font=('Arial', 12)).grid(row=0, column=0, padx=5)
entry_word1 = tk.Entry(input_frame, width=15, font=('Arial', 12))
entry_word1.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Word 2:", font=('Arial', 12)).grid(row=0, column=2, padx=5)
entry_word2 = tk.Entry(input_frame, width=15, font=('Arial', 12))
entry_word2.grid(row=0, column=3, padx=5)

btn_find = tk.Button(input_frame, text="查找桥接词", command=find_bridge_words, font=('Arial', 12))
btn_find.grid(row=0, column=4, padx=5)

btn_path = tk.Button(input_frame, text="最短路径查询", command=find_shortest_path, font=('Arial', 12))
btn_path.grid(row=0, column=5, padx=5)

# PageRank计算区域
input_frame_pagerank = tk.Frame(root)
input_frame_pagerank.pack(pady=10)

tk.Label(input_frame_pagerank, text="阻尼因子(damping):", font=('Arial', 12)).grid(row=0, column=0, padx=5)
entry_damping = tk.Entry(input_frame_pagerank, width=10, font=('Arial', 12))
entry_damping.grid(row=0, column=1, padx=5)
entry_damping.insert(0, "0.85")  # 默认值

btn_pagerank = tk.Button(input_frame_pagerank, text="计算PageRank", command=calculate_and_display_pagerank,
                         font=('Arial', 12))
btn_pagerank.grid(row=0, column=2, padx=5)

# 随机游走区域
btn_walk = tk.Button(root, text="开始随机游走", command=random_walk, font=('Arial', 12))
btn_walk.pack(pady=10)

btn_stop_walk = tk.Button(root, text="停止随机游走", command=stop_random_walk, font=('Arial', 12))
btn_stop_walk.pack(pady=10)

# 新文本插入桥接词区域
sentence_frame = tk.Frame(root)
sentence_frame.pack(pady=10)

tk.Label(sentence_frame, text="输入新文本：", font=('Arial', 12)).pack(side=tk.LEFT, padx=5)
entry_new_sentence = tk.Entry(sentence_frame, width=60, font=('Arial', 12))
entry_new_sentence.pack(side=tk.LEFT, padx=5)

btn_generate = tk.Button(sentence_frame, text="生成新文本", command=generate_new_text, font=('Arial', 12))
btn_generate.pack(side=tk.LEFT, padx=10)

# 结果显示
result_var = tk.StringVar()
result_label = tk.Label(root, textvariable=result_var, wraplength=960, justify="left", font=('Arial', 12), fg="blue")
result_label.pack(pady=10)

# 图显示区域
canvas_frame = tk.Frame(root)
canvas_frame.pack(pady=10)

root.mainloop()
"# B2 second edit on main.py" 

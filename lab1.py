"""
python lab1.py
一编：git实战测试手工修改文件

- 分支管理R7所做修改
---R5所做修改
二编：再次修改文件
三编：分支管理修改文件
四编：IDE中修改文件
"""

import re
import random
import sys
import os
from collections import defaultdict, deque
import heapq
import networkx as nx
import matplotlib.pyplot as plt


# import numpy as np

class DirectedGraph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(dict)  # {源节点: {目标节点: 权重}}
        self.in_edges = defaultdict(list)  # {目标节点: [源节点列表]}

    def add_edge(self, source, target, weight=1):
        """添加一条从source到target的边，权重为weight"""
        self.nodes.add(source)
        self.nodes.add(target)

        # 如果边已存在，增加权重
        if target in self.edges[source]:
            self.edges[source][target] += weight
        else:
            self.edges[source][target] = weight
            self.in_edges[target].append(source)

    def build_from_text(self, text):
        """从文本构建有向图"""
        # 预处理文本：将标点符号转为空格，非字母字符去除
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip().lower()

        words = text.split()
        if len(words) < 2:
            return

        # 构建边关系
        for i in range(len(words) - 1):
            self.add_edge(words[i], words[i + 1])

    def show_directed_graph(self):
        """展示有向图（文本形式）"""
        result = "有向图结构:\n"
        result += f"节点总数: {len(self.nodes)}\n"
        result += f"边总数: {sum(len(targets) for targets in self.edges.values())}\n"

        # 展示部分节点和边（节点按字母顺序）
        sorted_nodes = sorted(self.nodes)
        for node in sorted_nodes:
            neighbors = self.edges.get(node, {})
            if neighbors:
                result += f"节点 '{node}' 连接到: "
                edges_info = []
                for target, weight in neighbors.items():
                    edges_info.append(f"'{target}'(权重:{weight})")
                result += ", ".join(edges_info) + "\n"

        return result

    # def visualize_graph(self, highlight_path=None):
    #     """可视化有向图，使用networkx和matplotlib"""
    #     G = nx.DiGraph()

    #     # 添加节点和边
    #     for source in self.edges:
    #         for target, weight in self.edges[source].items():
    #             G.add_edge(source, target, weight=weight)

    #     # 绘图
    #     plt.figure(figsize=(12, 10))

    #     # 使用spring布局
    #     # np.random.seed(42)  # 设置随机数种子
    #     #pos = nx.spring_layout(G)

    #     pos = nx.spring_layout(G, seed=42)

    #     # 绘制节点
    #     nx.draw_networkx_nodes(G, pos, node_size=3000, node_color="white", edgecolors="black")

    #     # 绘制边和权重
    #     edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
    #     nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

    #     # 如果提供了高亮路径，用红色粗线显示
    #     if highlight_path and len(highlight_path) > 1:
    #         path_edges = [(highlight_path[i], highlight_path[i+1]) for i in range(len(highlight_path)-1)]
    #         nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=2.0, edge_color='red', arrows=True)

    #         # 绘制其他边
    #         other_edges = [(u, v) for u, v in G.edges() if (u, v) not in path_edges]
    #         nx.draw_networkx_edges(G, pos, edgelist=other_edges, width=1.0, arrows=True)
    #     else:
    #         # 绘制所有边
    #         nx.draw_networkx_edges(G, pos, width=1.0, arrows=True)

    #     # 绘制节点标签
    #     nx.draw_networkx_labels(G, pos, font_size=12)

    #     plt.axis('off')
    #     plt.tight_layout()

    #     # 保存图像
    #     plt.savefig("directed_graph.png", dpi=300, bbox_inches='tight')

    #     # 显示图像
    #     plt.show()

    #     return "图形已保存为 directed_graph.png"

    # def visualize_graph(self, highlight_path=None):
    #     """可视化有向图，优化美观性"""
    #     G = nx.DiGraph()

    #     # 添加节点和边
    #     for source in self.edges:
    #         for target, weight in self.edges[source].items():
    #             G.add_edge(source, target, weight=weight)

    #     plt.figure(figsize=(15, 12))

    #     # 尝试更高级的布局算法
    #     try:
    #         # Kamada-Kawai布局通常产生较少的边重叠
    #         pos = nx.kamada_kawai_layout(G)
    #     except:
    #         # 备选布局，在某些版本可能不支持上面的布局
    #         try:
    #             pos = nx.spring_layout(G)
    #         except:
    #             # 最后的备用选项
    #             pos = nx.circular_layout(G)

    #     # 绘制节点 - 使用更大的尺寸和白色填充
    #     nx.draw_networkx_nodes(G, pos, node_size=4000,
    #                         node_color="white",
    #                         edgecolors="black",
    #                         linewidths=2.0)

    #     # 绘制边 - 使用曲线边来减少重叠
    #     curved_edges = []
    #     straight_edges = []

    #     # 检测重复边（同两个节点之间有多条边的情况）
    #     edge_counts = {}
    #     for u, v in G.edges():
    #         if (u, v) in edge_counts:
    #             edge_counts[(u, v)] += 1
    #         else:
    #             edge_counts[(u, v)] = 1

    #     # 所有边都用弧线表示，减少重叠
    #     nx.draw_networkx_edges(G, pos, width=1.0, arrows=True,
    #                         connectionstyle='arc3,rad=0.1',
    #                         arrowsize=15, min_target_margin=20)

    #     # 高亮显示路径
    #     if highlight_path and len(highlight_path) > 1:
    #         path_edges = [(highlight_path[i], highlight_path[i+1]) for i in range(len(highlight_path)-1)]
    #         nx.draw_networkx_edges(G, pos, edgelist=path_edges,
    #                             width=3.0, edge_color='red',
    #                             arrows=True,
    #                             connectionstyle='arc3,rad=0.1',
    #                             arrowsize=20, min_target_margin=20)

    #     # 绘制节点标签 - 清晰的字体
    #     nx.draw_networkx_labels(G, pos, font_size=14, font_family='sans-serif', font_weight='bold')

    #     # 绘制边权重 - 统一放置在边的中间位置，稍微偏上
    #     edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
    #     nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
    #                                 font_size=12,
    #                                 font_family='sans-serif',
    #                                 font_color='black',
    #                                 label_pos=0.5,  # 标签位置在边的中间
    #                                 bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.8),
    #                                 rotate=False)  # 不旋转标签，保持一致方向

    #     plt.axis('off')
    #     plt.tight_layout()

    #     # 设置更大的边界，避免节点被裁剪
    #     plt.margins(0.15)

    #     # 保存高分辨率图像
    #     plt.savefig("directed_graph.png", dpi=300, bbox_inches='tight')
    #     plt.show()

    #     return "图形已保存为 directed_graph.png"

    def visualize_graph_with_dot(self, highlight_path=None):
        """使用Graphviz的dot引擎可视化有向图，确保箭头清晰可见"""
        try:
            import graphviz
        except ImportError:
            return "请先安装graphviz库: pip install graphviz"

        # 创建有向图
        dot = graphviz.Digraph(comment='Directed Graph', format='png')
        dot.attr(rankdir='LR', size='10,8', ratio='fill')
        dot.attr('node', shape='ellipse', style='filled', fillcolor='white',
                 fontsize='14', fontname='SimSun', width='0.8', height='0.8')
        dot.attr('edge', fontsize='12', fontname='SimSun')

        # 添加节点
        for node in self.nodes:
            dot.node(node)

        # 添加边
        for source in self.edges:
            for target, weight in self.edges[source].items():
                if highlight_path and len(highlight_path) > 1:
                    # 检查是否是高亮路径的一部分
                    is_highlight = False
                    for i in range(len(highlight_path) - 1):
                        if source == highlight_path[i] and target == highlight_path[i + 1]:
                            is_highlight = True
                            break

                    if is_highlight:
                        dot.edge(source, target, label=str(weight), color='red', penwidth='2.0')
                    else:
                        dot.edge(source, target, label=str(weight))
                else:
                    dot.edge(source, target, label=str(weight))

        # 渲染并保存图形
        try:
            dot.render('directed_graph', cleanup=True)
            return "图形已保存为 directed_graph.png"
        except Exception as e:
            return f"生成图形时出错: {e}"

    def query_bridge_words(self, word1, word2):
        """查询两个单词之间的桥接词"""
        word1, word2 = word1.lower(), word2.lower()

        # 检查单词是否在图中
        if word1 not in self.nodes and word2 not in self.nodes:
            return f"No \"{word1}\" and \"{word2}\" in the graph!"
        if word1 not in self.nodes:
            return f"No \"{word1}\" in the graph!"
        if word2 not in self.nodes:
            return f"No \"{word2}\" in the graph!"

        # 查找桥接词
        bridge_words = []
        for bridge in self.edges.get(word1, {}):
            if word2 in self.edges.get(bridge, {}):
                bridge_words.append(bridge)

        if not bridge_words:
            return f"No bridge words from \"{word1}\" to \"{word2}\"!"
        elif len(bridge_words) == 1:
            return f"The bridge words from \"{word1}\" to \"{word2}\" is: \"{bridge_words[0]}\""
        else:
            last_word = bridge_words.pop()
            bridges_str = ", ".join([f"\"{word}\"" for word in bridge_words])
            return f"The bridge words from \"{word1}\" to \"{word2}\" are: {bridges_str} and \"{last_word}\"."

    def generate_new_text(self, input_text):
        """根据bridge word生成新文本"""
        # 预处理输入文本
        input_text = re.sub(r'[^a-zA-Z\s]', ' ', input_text)
        input_text = re.sub(r'\s+', ' ', input_text).strip().lower()
        words = input_text.split()

        if len(words) < 2:
            return input_text

        result = [words[0]]

        for i in range(len(words) - 1):
            word1, word2 = words[i], words[i + 1]

            # 查找桥接词
            bridge_candidates = []
            if word1 in self.nodes and word2 in self.nodes:
                for bridge in self.edges.get(word1, {}):
                    if word2 in self.edges.get(bridge, {}):
                        bridge_candidates.append(bridge)

            # 如果有桥接词，随机选一个插入
            if bridge_candidates:
                bridge = random.choice(bridge_candidates)
                result.append(bridge)

            result.append(word2)

        return " ".join(result)

    def calc_shortest_path(self, word1, word2=None):
        """计算最短路径，如果只提供word1，则计算word1到所有其他节点的最短路径"""
        word1 = word1.lower()

        # 检查起始单词是否在图中
        if word1 not in self.nodes:
            return f"No \"{word1}\" in the graph!", None

        # 如果提供了第二个单词，执行单对最短路径计算
        if word2:
            word2 = word2.lower()
            if word2 not in self.nodes:
                return f"No \"{word2}\" in the graph!", None
            if word1 == word2:
                return f"The path from \"{word1}\" to \"{word2}\" is: {word1}", [word1]

            # 使用Dijkstra算法计算最短路径
            distances = {node: float('infinity') for node in self.nodes}
            previous_nodes = {node: None for node in self.nodes}
            distances[word1] = 0
            unvisited = [(0, word1)]  # (距离, 节点)

            while unvisited:
                current_distance, current_node = heapq.heappop(unvisited)

                # 如果找到目标节点，构建路径
                if current_node == word2:
                    path = []
                    while current_node:
                        path.append(current_node)
                        current_node = previous_nodes[current_node]
                    path.reverse()
                    return f"The shortest path from \"{word1}\" to \"{word2}\" is: {' → '.join(path)}\nPath length: {current_distance}", path

                # 如果当前节点已处理过，跳过
                if current_distance > distances[current_node]:
                    continue

                # 检查所有邻居节点
                for neighbor, weight in self.edges.get(current_node, {}).items():
                    distance = current_distance + weight

                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        previous_nodes[neighbor] = current_node
                        heapq.heappush(unvisited, (distance, neighbor))

            return f"No path from \"{word1}\" to \"{word2}\"!", None

        # 如果只提供了一个单词，计算到所有其他节点的最短路径
        else:
            # 使用Dijkstra算法计算到所有节点的最短路径
            distances = {node: float('infinity') for node in self.nodes}
            previous_nodes = {node: None for node in self.nodes}
            distances[word1] = 0
            unvisited = [(0, word1)]  # (距离, 节点)

            while unvisited:
                current_distance, current_node = heapq.heappop(unvisited)

                # 如果当前节点已处理过，跳过
                if current_distance > distances[current_node]:
                    continue

                # 检查所有邻居节点
                for neighbor, weight in self.edges.get(current_node, {}).items():
                    distance = current_distance + weight

                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        previous_nodes[neighbor] = current_node
                        heapq.heappush(unvisited, (distance, neighbor))

            # 构建并展示所有路径
            result = f"从 \"{word1}\" 到所有可达节点的最短路径:\n"
            found_paths = 0

            # 按照路径长度排序，先展示短路径
            path_info = []
            for target in self.nodes:
                if target == word1:
                    continue

                if distances[target] < float('infinity'):
                    path = []
                    current = target
                    while current:
                        path.append(current)
                        current = previous_nodes[current]
                    path.reverse()

                    path_info.append((target, distances[target], path))
                    found_paths += 1

            # 按路径长度排序
            path_info.sort(key=lambda x: x[1])

            # 显示所有路径
            for target, distance, path in path_info:
                result += f"到 \"{target}\": {' → '.join(path)}，路径长度: {distance}\n"

            if found_paths == 0:
                result += f"从 \"{word1}\" 无法到达任何其他节点!\n"

            return result, None

    def calc_page_rank(self, word=None, d=0.85, max_iterations=100, tol=1e-6, use_weighted_init=False):
        """计算PageRank值，可选使用基于词频的加权初始值"""
        # 初始化PageRank值
        if use_weighted_init:
            # 计算每个节点的出现频率（基于出边权重总和）
            total_weights = {}
            for node in self.nodes:
                # 计算入边权重
                in_weight = sum(self.edges[src][node] for src in self.in_edges.get(node, []) if node in self.edges[src])
                # 计算出边权重
                out_weight = sum(weight for target, weight in self.edges.get(node, {}).items())
                # 总权重是入边和出边权重之和
                total_weights[node] = in_weight + out_weight

            # 计算总权重和
            weight_sum = sum(total_weights.values())

            # 如果权重总和为0，则使用均匀分布
            if weight_sum == 0:
                pr = {node: 1 / len(self.nodes) for node in self.nodes}
            else:
                # 基于权重分配初始PR值，确保总和为1
                pr = {node: total_weights[node] / weight_sum for node in self.nodes}
        else:
            # 使用传统均匀分布的初始值
            pr = {node: 1 / len(self.nodes) for node in self.nodes}

        # 计算PageRank
        for _ in range(max_iterations):
            prev_pr = pr.copy()

            # 收集出度为0的节点的PR值总和
            sink_pr_sum = 0
            for node in self.nodes:
                if len(self.edges.get(node, {})) == 0:  # 出度为0的节点
                    sink_pr_sum += prev_pr[node]

            # 计算每个节点新的PR值
            for node in self.nodes:
                in_sum = 0
                # 处理指向当前节点的入边贡献
                for in_node in self.in_edges.get(node, []):
                    out_count = len(self.edges.get(in_node, {}))
                    if out_count > 0:  # 有出边的节点
                        in_sum += prev_pr[in_node] / out_count

                # 加上出度为0的节点均分的PR值贡献
                pr[node] = (1 - d) / len(self.nodes) + d * (in_sum + sink_pr_sum / len(self.nodes))

            # 检查收敛性
            diff = sum(abs(pr[node] - prev_pr[node]) for node in self.nodes)
            if diff < tol:
                break

        # 如果指定了单词，则返回该单词的PR值
        if word:
            word = word.lower()
            if word in pr:
                return pr[word]
            else:
                return f"No \"{word}\" in the graph!"

        # 否则返回所有单词的PR值（按PR值降序排序）
        sorted_pr = sorted(pr.items(), key=lambda x: x[1], reverse=True)
        result = "PageRank值 (d=0.85"
        if use_weighted_init:
            result += ", 使用词频加权初始值"
        result += "):\n"

        for node, rank in sorted_pr[:20]:  # 只展示前20个
            result += f"{node}: {rank:.4f}\n"

        return result

    def random_walk(self):
        """随机游走"""
        if not self.nodes:
            return "图为空，无法进行随机游走!"

        # 随机选择起点
        current = random.choice(list(self.nodes))
        path = [current]
        visited_edges = set()  # 存储访问过的边 (起点,终点)

        while True:
            # 获取当前节点的所有出边
            neighbors = list(self.edges.get(current, {}).keys())

            # 如果没有出边，结束游走
            if not neighbors:
                break

            # 随机选择下一个节点
            next_node = random.choice(neighbors)
            current_edge = (current, next_node)

            # 如果这条边已经访问过，结束游走（但是要把最后一个节点加入路径）
            if current_edge in visited_edges:
                path.append(next_node)  # 添加最后一个节点，形成环
                break

            # 将当前边加入已访问集合
            visited_edges.add(current_edge)

            # 移动到下一个节点
            path.append(next_node)
            current = next_node

        # 将路径保存到文件
        result = " ".join(path)
        with open("random_walk_result.txt", "w") as f:
            f.write(result)

        # 可视化随机游走路径
        highlight_path = path
        self.visualize_graph(highlight_path=highlight_path)

        return f"随机游走路径: {result}\n路径已保存到 random_walk_result.txt\n随机游走图已保存为 directed_graph.png"


def main():
    graph = DirectedGraph()

    # 处理命令行参数
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input("请输入文本文件路径: ")

    # 读取文件内容
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    except Exception as e:
        print(f"读取文件错误: {e}")
        return

    # 构建图
    graph.build_from_text(text)

    while True:
        print("\n请选择功能:")
        print("1. 展示有向图(文本形式)")
        print("2. 展示有向图(图形形式)")
        print("3. 查询桥接词")
        print("4. 根据桥接词生成新文本")
        print("5. 计算最短路径")
        print("6. 计算PageRank值")
        print("7. 随机游走")
        print("0. 退出")

        choice = input("请输入选择: ")

        if choice == '1':
            print(graph.show_directed_graph())

        elif choice == '2':
            print(graph.visualize_graph())

        elif choice == '3':
            word1 = input("请输入第一个单词: ")
            word2 = input("请输入第二个单词: ")
            print(graph.query_bridge_words(word1, word2))

        elif choice == '4':
            text = input("请输入一段文本: ")
            print(graph.generate_new_text(text))

        elif choice == '5':
            word1 = input("请输入起始单词: ")
            word2 = input("请输入目标单词(直接回车将计算到所有节点的最短路径): ")

            if word2:
                path_info, path = graph.calc_shortest_path(word1, word2)
                print(path_info)
                if path and len(path) > 1:
                    print("正在绘制最短路径...")
                    graph.visualize_graph(highlight_path=path)
            else:
                path_info, _ = graph.calc_shortest_path(word1)
                print(path_info)

        elif choice == '6':
            word = input("请输入单词(直接回车计算所有单词的PR值): ")
            use_weighted = input("是否使用词频加权初始PR值？(y/n): ").lower() == 'y'

            if word:
                pr = graph.calc_page_rank(word, use_weighted_init=use_weighted)
                if isinstance(pr, float):
                    print(f"{word}的PageRank值: {pr:.4f}")
                else:
                    print(pr)
            else:
                print(graph.calc_page_rank(use_weighted_init=use_weighted))

        elif choice == '7':
            print(graph.random_walk())

        elif choice == '0':
            break

        else:
            print("无效选择，请重试")


if __name__ == "__main__":
    main()"# B2 second edit on lab1.py" 

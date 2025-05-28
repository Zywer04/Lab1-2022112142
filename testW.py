import unittest
from unittest.mock import MagicMock, patch
import networkx as nx
import random

# 假设你的函数和依赖在同一个模块中，这里直接定义简化版clean_text
def clean_text(text):
    # 简单拆分小写单词，实际可替换为你原函数
    return text.lower().split()

# 伪装的全局变量和控件对象
G = None
result_var = None
entry_new_sentence = None

def generate_new_text():
    global G, result_var, entry_new_sentence
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


class TestGenerateNewText(unittest.TestCase):
    def setUp(self):
        global G, result_var, entry_new_sentence
        # 每个测试前重置全局变量

        # 模拟result_var有set方法，记录最后设置的值
        class ResultVarMock:
            def __init__(self):
                self.value = None
            def set(self, val):
                self.value = val

        # 模拟entry_new_sentence有get方法，返回测试输入
        class EntryMock:
            def __init__(self, text):
                self.text = text
            def get(self):
                return self.text

        result_var = ResultVarMock()
        entry_new_sentence = EntryMock("")  # 默认空，后续测试覆盖
        G = None  # 默认无图

        self.result_var = result_var
        self.entry_new_sentence = entry_new_sentence

    def test_path1_G_is_None(self):
        global G, result_var, entry_new_sentence
        G = None
        self.entry_new_sentence.text = "any input"
        generate_new_text()
        self.assertEqual(self.result_var.value, "请先加载文本文件并生成图！")

    def test_path2_words_less_than_2(self):
        global G, result_var, entry_new_sentence
        G = nx.DiGraph()
        self.entry_new_sentence.text = "hello"
        generate_new_text()
        self.assertEqual(self.result_var.value, "请输入至少两个单词！")

    def test_path3_no_bridge_insert(self):
        global G, result_var, entry_new_sentence
        G = nx.DiGraph()
        # 图中有节点，但无桥接词
        G.add_nodes_from(["good", "day"])
        self.entry_new_sentence.text = "good day"
        generate_new_text()
        self.assertEqual(self.result_var.value, "生成新文本：\ngood day")

    @patch('random.choice', lambda x: x[0])  # 固定选桥接词第一个，保证可测试
    def test_path4_bridge_insert(self):
        global G, result_var, entry_new_sentence
        G = nx.DiGraph()
        # 构建桥接词桥梁： good -> bridge -> day
        G.add_nodes_from(["good", "bridge", "day"])
        G.add_edge("good", "bridge")
        G.add_edge("bridge", "day")
        self.entry_new_sentence.text = "good day"
        generate_new_text()
        self.assertEqual(self.result_var.value, "生成新文本：\ngood bridge day")


if __name__ == '__main__':
    unittest.main()

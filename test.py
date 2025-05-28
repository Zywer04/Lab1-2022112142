import unittest
import networkx as nx


def find_bridge_words_pure(G, word1, word2):
    """
    找桥接词的纯函数版本，不依赖GUI控件。

    参数:
        G: networkx.DiGraph 有向图
        word1: str，第一个词
        word2: str，第二个词

    返回:
        str，结果文本
    """
    if G is None:
        return "请先加载文本文件并生成图！"

    word1 = word1.lower().strip()
    word2 = word2.lower().strip()

    if word1 not in G or word2 not in G:
        return f"No {word1} or {word2} in the graph!"

    bridge_words = [w3 for w3 in G.successors(word1) if G.has_edge(w3, word2)]

    if not bridge_words:
        return f"No bridge words from {word1} to {word2}!"
    else:
        if len(bridge_words) == 1:
            return f"The bridge word from {word1} to {word2} is: {bridge_words[0]}."
        else:
            formatted = ", ".join(bridge_words[:-1]) + f", and {bridge_words[-1]}"
            return f"The bridge words from {word1} to {word2} are: {formatted}."


class TestFindBridgeWordsPure(unittest.TestCase):

    def setUp(self):
        # 构造测试图
        self.G = nx.DiGraph()
        # 添加节点和边，方便测试
        self.G.add_nodes_from(["a", "b", "love", "peace", "hello", "world"])
        # 为了测试桥接词：
        # a -> love -> b
        self.G.add_edge("a", "love")
        self.G.add_edge("love", "b")
        # a -> peace -> b
        self.G.add_edge("a", "peace")
        self.G.add_edge("peace", "b")
        # hello和world节点无桥接关系，且hello和world单独存在

    def test_no_graph_loaded(self):
        # 1. 未加载图
        self.assertEqual(find_bridge_words_pure(None, "a", "b"), "请先加载文本文件并生成图！")

    def test_word_not_in_graph(self):
        # 2. "hello", "world"其中一个不在图中，比如"hi"不存在
        self.assertEqual(find_bridge_words_pure(self.G, "hello", "unseen"), "No hello or unseen in the graph!")
        self.assertEqual(find_bridge_words_pure(self.G, "unseen", "world"), "No unseen or world in the graph!")
        self.assertEqual(find_bridge_words_pure(self.G, "hello", "world"), "No bridge words from hello to world!")

    def test_no_bridge_words(self):
        # 3. "a", "b"在图中，但去掉桥接边使无桥接词
        G2 = nx.DiGraph()
        G2.add_nodes_from(["a", "b", "c"])
        G2.add_edge("a", "c")  # 但没有 c->b
        self.assertEqual(find_bridge_words_pure(G2, "a", "b"), "No bridge words from a to b!")

    def test_one_bridge_word(self):
        # 4. 一个桥接词 love
        G3 = nx.DiGraph()
        G3.add_nodes_from(["a", "b", "love"])
        G3.add_edge("a", "love")
        G3.add_edge("love", "b")
        self.assertEqual(find_bridge_words_pure(G3, "a", "b"), "The bridge word from a to b is: love.")

    def test_multiple_bridge_words(self):
        # 5. 多个桥接词 love, peace
        self.assertEqual(
            find_bridge_words_pure(self.G, "a", "b"),
            "The bridge words from a to b are: love, and peace."
        )


if __name__ == "__main__":
    unittest.main()

graph TD
    A[开始] --> B[读取输入词 word1 和 word2]
    B --> C[从输入框中获取两个词并转小写，去除空白]
    C --> D[检查图是否已生成 (G is None)]
    D -->|是| E[显示提示: 请先加载文本文件并生成图！]
    E --> F[结束]
    D -->|否| G[检查两个词是否在图中]
    G --> H[任一不在 → 显示提示: No word1 or word2 in the graph!]
    H --> F
    G --> I[都在 → 继续]
    I --> J[查找桥接词: 从 word1 的后继节点中找出能直接到达 word2 的词]
    J --> K[判断是否存在桥接词]
    K -->|没有| L[显示提示: No bridge words from word1 to word2!]
    L --> F
    K -->|有| M[格式化输出结果]
    M --> N[若只有一个桥接词 → 显示: The bridge word from word1 to word2 is: XXX.]
    M --> O[若有多个桥接词 → 显示: The bridge words from word1 to word2 are: XXX, YYY, and ZZZ.]
    O --> P[将结果显示到界面上]
    P --> F

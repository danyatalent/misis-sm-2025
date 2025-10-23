from math import log2, log, e
from typing import List, Tuple, Dict

def dfs(a: int, b: int, adj: Dict[int, List[int]], reach: List[List[bool]]):
    for c in adj[b]:
        if not reach[a - 1][c - 1]:
            reach[a - 1][c - 1] = True
            dfs(a, c, adj, reach)


def task1(s: str, e: str) -> Tuple[
    List[List[bool]], 
    List[List[bool]],
    List[List[bool]], 
    List[List[bool]],
    List[List[bool]]
]:
    edges = [tuple(map(int, x.split(','))) for x in s.strip().split('\n')]
    n = max(max(u, v) for u, v in edges)

    dir_parent = [[False] * n for _ in range(n)]
    for u, v in edges:
        dir_parent[u - 1][v - 1] = True

    dir_child = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dir_child[i][j] = dir_parent[j][i]

    adj = {i: [] for i in range(1, n + 1)}
    for u, v in edges:
        adj[u].append(v)

    reach = [[False] * n for _ in range(n)]
    for i in range(1, n + 1):
        dfs(i, i, adj, reach)

    indir_parent = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if reach[i][j] and not dir_parent[i][j] and i != j:
                indir_parent[i][j] = True

    indir_child = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            indir_child[i][j] = indir_parent[j][i]

    co_parent = [[False] * n for _ in range(n)]
    par = {}
    for u, v in edges:
        par[v] = u

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i != j and i in par and j in par and par[i] == par[j]:
                co_parent[i - 1][j - 1] = True

    return dir_parent, dir_child, indir_parent, indir_child, co_parent


def main(s: str, root: str) -> Tuple[float, float]:
    dir_parent, dir_child, indir_parent, indir_child, co_parent = task1(s, root)

    relations = [dir_parent, dir_child, indir_parent, indir_child, co_parent]
    n = len(dir_parent)
    k = len(relations)

    H_sum = 0.0
    for j in range(n):
        for r in relations:
            lij = sum(1 for val in r[j] if val)
            if lij > 0:
                P = lij / (n - 1)
                H_sum += -P * log2(P)

    c = 1 / (e * log(2))
    H_ref = c * n * k
    h = H_sum / H_ref

    return round(H_sum, 1), round(h, 1)


if __name__ == "__main__":
    s = "1,2\n1,3\n3,4\n3,5"
    root = "1"
    H, h = main(s, root)

    print("Энтропия:", H)
    print("Нормированная сложность:", h)
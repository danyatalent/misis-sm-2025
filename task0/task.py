import sys
import os
import csv
from typing import List, Any, Optional


def _parse_token(tok: str) -> Any:
    s = tok.strip()
    if s == "":
        raise ValueError("empty token")
    try:
        return int(s)
    except ValueError:
        return s


def _read_edges_from_string(s: str) -> List[tuple]:
    reader = csv.reader(s.splitlines(), skipinitialspace=True)
    edges = []
    for row in reader:
        if not row:
            continue
        cells = [c.strip() for c in row if c.strip() != ""]
        if len(cells) < 2:
            continue
        u = _parse_token(cells[0])
        v = _parse_token(cells[1])
        edges.append((u, v))
    return edges


def _read_edges_from_file(path: str) -> List[tuple]:
    edges = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, skipinitialspace=True)
        for row in reader:
            if not row:
                continue
            cells = [c.strip() for c in row if c.strip() != ""]
            if len(cells) < 2:
                continue
            u = _parse_token(cells[0])
            v = _parse_token(cells[1])
            edges.append((u, v))
    return edges


def adjacency_matrix_from_csv(input_data: str, directed: bool = False) -> List[List[int]]:
    """
    input_data: либо путь до файла, либо строка в формате CSV (с переносами строк)
    Возвращает матрицу смежности (список списков), порядок вершин — отсортированный
    (сначала числовые метки по возрастанию, затем строковые по лексикографическому порядку).
    По умолчанию граф считается неориентированным.
    """
    if os.path.exists(input_data):
        edges = _read_edges_from_file(input_data)
    else:
        edges = _read_edges_from_string(input_data)

    if not edges:
        return []

    verts_set = {v for e in edges for v in e}

    def _sort_key(x):
        return (0, x) if isinstance(x, int) else (1, str(x))

    vertices = sorted(verts_set, key=_sort_key)
    idx = {v: i for i, v in enumerate(vertices)}
    n = len(vertices)
    matrix = [[0] * n for _ in range(n)]

    for u, v in edges:
        ui = idx[u]
        vi = idx[v]
        matrix[ui][vi] = 1
        if not directed:
            matrix[vi][ui] = 1

    return matrix


def main(arg: Optional[str] = None) -> List[List[int]]:
    if arg is None:
        if len(sys.argv) < 2:
            raise ValueError(
                "No input provided. Usage: python task0/task.py '<csv_string>' or python task0/task.py path/to/file.csv"
            )
        arg = sys.argv[1]
    return adjacency_matrix_from_csv(arg)


if __name__ == "__main__":
    try:
        mat = main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)

    for row in mat:
        print(" ".join(str(x) for x in row))

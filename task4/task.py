import json
import numpy as np


def build_matrix(ranking, items):
    n = len(items)
    index = {item: i for i, item in enumerate(items)}
    matrix = np.zeros((n, n), dtype=int)

    for i, group in enumerate(ranking):
        if not isinstance(group, list):
            group = [group]

        for g in group:
            for k in items:
                gi, ki = index[g], index[k]
                matrix[gi][ki] = 1
                
                for prev_group in ranking[:i]:
                    if not isinstance(prev_group, list):
                        prev_group = [prev_group]
                    for p in prev_group:
                        matrix[gi][index[p]] = 0
                        matrix[index[p]][gi] = 1
    return matrix


def find_contradictions(A, B, items):
    n = len(items)
    contr = []
    for i in range(n):
        for j in range(i + 1, n):
            if A[i][j] == 1 and A[j][i] == 0 and B[i][j] == 0 and B[j][i] == 1:
                contr.append([items[i], items[j]])
            elif A[i][j] == 0 and A[j][i] == 1 and B[i][j] == 1 and B[j][i] == 0:
                contr.append([items[j], items[i]])
    return contr


def flatten(ranking):
    result = []
    for group in ranking:
        if isinstance(group, list):
            result.extend(group)
        else:
            result.append(group)
    return result


def build_final_ranking(items, contr):
    contr_map = {}
    for a, b in contr:
        contr_map.setdefault(a, []).append(b)

    result = []
    used = set()
    for item in items:
        if item in used:
            continue
        if item in contr_map:
            cluster = [item] + [b for b in contr_map[item] if b not in used]
            used.update(cluster)
            result.append(cluster)
        else:
            result.append(item)
            used.add(item)
    return result


def main(json_a: str, json_b: str) -> str:
    ranking_a = json.loads(json_a)
    ranking_b = json.loads(json_b)

    items = sorted(set(flatten(ranking_a)) | set(flatten(ranking_b)))

    A = build_matrix(ranking_a, items)
    B = build_matrix(ranking_b, items)

    contr = find_contradictions(A, B, items)
    final_ranking = build_final_ranking(items, contr)
    return json.dumps(final_ranking, ensure_ascii=False)


if __name__ == "__main__":
    a = json.dumps([1,[2,3],4,[5,6,7],8,9,10])
    b = json.dumps([[1,2],[3,4,5],6,7,9,[8,10]])
    print(main(a, b))
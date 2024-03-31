import numpy as np
from multiprocessing import Process, Queue


def element(index, A, B, result_queue):
    i, j = index
    res = 0
    N = len(A[0]) or len(B)
    for k in range(N):
        res += A[i][k] * B[k][j]
    result_queue.put(res)


def multiply_matrices(matrix1, matrix2):
    # создаем пустую матрицу, которую заполним результатами
    result_matrix = np.zeros((len(matrix1), len(matrix2[0])))

    processes = []
    result_queue = Queue()

    # для каждого элемента матрицы запускаем свой процесс
    for i, row1 in enumerate(matrix1):
        for j, col2 in enumerate(matrix1):
            process = Process(target=element, args=((i, j), matrix1, matrix2, result_queue))
            processes.append(process)
            process.start()

    for process in processes:
        process.join()

    # заполняем матрицу полученными значениями
    for i in range(len(matrix1)):
        for j in range(len(matrix2[0])):
            result_matrix[i][j] = result_queue.get()

    return result_matrix


if __name__ == "__main__":
    matrix1 = np.random.randint(0, 10, size=(6, 6))
    matrix2 = np.random.randint(0, 10, size=(6, 6))
    # matrix1 = [[1, 1, 1, 1, 1]] * 5
    # matrix2 = [[1, 1, 1, 1, 1]] * 5

    result = multiply_matrices(matrix1, matrix2)
    print(result)

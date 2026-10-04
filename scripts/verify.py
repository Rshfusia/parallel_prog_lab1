import os
import subprocess
import sys
import numpy as np

# python scripts/verify.py

EXE_PATH = os.path.join("build", "windows-debug", "src", "src.exe")
FILE_A = os.path.join("data", "matrix_A.txt")
FILE_B = os.path.join("data", "matrix_B.txt")
FILE_C = os.path.join("data", "matrix_C.txt")


def load_matrix_from_file(filepath):
    """Считывает матрицу из файла в массив NumPy."""
    with open(filepath, "r") as f:
        content = f.read().strip().split()
        data = [float(x) for x in content]
    total = len(data)
    side = int(np.round(np.sqrt(total)))
    if side * side != total and int(data[0]) ** 2 == total - 1:
        side = int(data[0])
        data = data[1:]
    return np.array(data).reshape((side, side))


def main():
    print("=" * 50)
    print(" АВТОМАТИЗИРОВАННАЯ ВЕРИФИКАЦИЯ ВЫЧИСЛЕНИЙ")
    print("=" * 50)

    if not os.path.exists(EXE_PATH):
        print(f"[ОШИБКА] Исполняемый файл C++ не найден: {EXE_PATH}")
        print("Сначала соберите проект в VS Code (клавиша F7).")
        sys.exit(1)

    print("[1/4] Запуск C++ программы...")
    result = subprocess.run([EXE_PATH, FILE_A, FILE_B, FILE_C], capture_output=True, text=True, encoding="utf-8")

    if result.returncode != 0:
        print("[ОШИБКА] C++ программа завершилась с ошибкой:")
        print(result.stderr)
        sys.exit(1)

    print(result.stdout.strip())

    print("\n[2/4] Загрузка данных и эталонное перемножение (NumPy)...")
    matrix_A = load_matrix_from_file(FILE_A)
    matrix_B = load_matrix_from_file(FILE_B)

    reference_C = np.matmul(matrix_A, matrix_B)

    print("[3/4] Загрузка результата из C++...")
    cpp_C = load_matrix_from_file(FILE_C)

    print("[4/4] Сверка матриц...")
    max_diff = np.max(np.abs(reference_C - cpp_C))
    is_correct = np.allclose(reference_C, cpp_C, atol=1e-5)

    print("\n" + "=" * 50)
    if is_correct:
        print(" РЕЗУЛЬТАТ: УСПЕШНО (ВЕРИФИКАЦИЯ ПРОЙДЕНА)")
        print(f" Максимальное абсолютное расхождение: {max_diff:.2e}")
    else:
        print(" РЕЗУЛЬТАТ: ОШИБКА (ВЫЧИСЛЕНИЯ НЕ СОВПАДАЮТ)")
        print(f" Максимальное расхождение: {max_diff}")
    print("=" * 50)

    if matrix_A.shape[0] <= 5:
        print("\nМатрица C (C++):")
        print(cpp_C)
        print("\nМатрица C (NumPy эталон):")
        print(reference_C)

if __name__ == "__main__":
    main()
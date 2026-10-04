import std;

std::vector<double> load_matrix(const std::filesystem::path& path, int& n) {
    std::ifstream file(path);
    std::vector<double> data;
    double val;
    while (file >> val) {
        data.push_back(val);
    }
    int explicit_n = static_cast<int>(data[0]);
    if (static_cast<size_t>(explicit_n * explicit_n) == data.size() - 1) {
        n = explicit_n;
        data.erase(data.begin());
    } else {
        n = static_cast<int>(std::round(std::sqrt(data.size())));
    }
    return data;
}

void save_matrix(const std::filesystem::path& path, int n, const std::vector<double>& mat) {
    std::ofstream file(path);
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            file << std::format("{:.6f} ", mat[i * n + j]);
        }
        file << "\n";
    }
}

void multiply(int n, const std::vector<double>& A, const std::vector<double>& B, std::vector<double>& C) {
    std::fill(C.begin(), C.end(), 0.0);
    for (int i = 0; i < n; ++i) {
        for (int k = 0; k < n; ++k) {
            double a_ik = A[i * n + k];
            for (int j = 0; j < n; ++j) {
                C[i * n + j] += a_ik * B[k * n + j];
            }
        }
    }
}

int main(int argc, char* argv[]) {
    std::filesystem::path path_a = (argc > 1) ? argv[1] : "data/matrix_A.txt";
    std::filesystem::path path_b = (argc > 2) ? argv[2] : "data/matrix_B.txt";
    std::filesystem::path path_c = (argc > 3) ? argv[3] : "data/matrix_C.txt";
    int n_a = 0, n_b = 0;
    auto A = load_matrix(path_a, n_a);
    auto B = load_matrix(path_b, n_b);
    int n = n_a;
    std::vector<double> C(n * n, 0.0);
    auto start = std::chrono::high_resolution_clock::now();
    multiply(n, A, B, C);
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> duration = end - start;
    save_matrix(path_c, n, C);
    std::println("Task size (N)   : {}x{}", n, n);
    std::println("Execution time  : {:.3f} ms", duration.count());
    return 0;
}
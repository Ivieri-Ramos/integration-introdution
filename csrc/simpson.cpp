#include <vector>
#include <string>
#include <functional>
#include <stdexcept>
#include <cmath>
#include <cstdint>
#define exprtk_disable_fallthrough
#include "exprtk.hpp" // biblioteca para validação de funções

class SimpsonIntegrator {
public:
    // Integração com vetores discretos (x, y)
    static double integrate(const std::vector<double>& x, const std::vector<double>& y) {
        if (x.size() != y.size()) {
            throw std::invalid_argument("Os vetores x e y devem ter o mesmo tamanho.");
        }
        size_t n_points = x.size();
        if (n_points < 3 || n_points % 2 == 0) {
            throw std::invalid_argument("O numero de pontos deve ser impar e pelo menos 3.");
        }

        // Verifica se todos os intervelos tem o mesmo tamanho
        double h = x[1] - x[0];
        for (size_t i = 1; i < n_points - 1; ++i) {
            if (std::abs((x[i + 1] - x[i]) - h) > 1e-7) {
                throw std::invalid_argument("Os pontos do vetor x devem ter espaçamento uniforme.");
            }
        }

        // Faz a somatoria de todos os intervalos
        double sum = y.front() + y.back();
        for (size_t i = 1; i < n_points - 1; ++i) {
            sum += (i % 2 != 0) ? 4.0 * y[i] : 2.0 * y[i];
        }

        return (h / 3.0) * sum;
    }

    // Integração com função, intervalo de [a,b] com n subintervalos
    static double integrate(const std::function<double(double)>& func, const double a, const double b, uint64_t n) {
        if (n == 0 || n % 2 != 0) {
            throw std::invalid_argument("O numero de intervalos n deve ser par e diferente de 0.");
        }

        double h = (b - a) / n;
        double sum = func(a) + func(b);

        for (uint64_t i = 1; i < n; ++i) {
            double x = a + i * h;
            sum += (i % 2 != 0) ? 4.0 * func(x) : 2.0 * func(x);
        }

        return (h / 3.0) * sum;
    }

    // 3. Integração com validação de string de expressão via ExprTk, lê a expressão digitada no terminal
    static double integrate(const std::string& expression_str, const double a, const double b, uint64_t n, const std::string& var_name = "x") {
        double x_val = 0.0;
        
        // Interpreta os elementos escritos
        exprtk::symbol_table<double> symbol_table;
        symbol_table.add_variable(var_name, x_val);
        symbol_table.add_constants();
        symbol_table.add_constant("E", std::exp(1.0));

        exprtk::expression<double> expression;
        expression.register_symbol_table(symbol_table);

        exprtk::parser<double> parser;
        if (!parser.compile(expression_str, expression)) {
            throw std::runtime_error("Erro ao validar a expressao: " + parser.error());
        }

        // Encapsula os elementos da expressão compilada como std::function
        auto func = [&](double x) {
            x_val = x;
            return expression.value();
        };

        // Chama novamente a função de integração com os a função conhecida
        return integrate(func, a, b, n);
    }
};

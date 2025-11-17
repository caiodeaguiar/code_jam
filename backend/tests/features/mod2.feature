Feature: Calculadora de Módulo 2
    Para verificar a funcionalidade da API de cálculo
    Como um usuário
    Eu quero saber se um número é par ou ímpar

Scenario Outline: Verificar números
    When Eu chamo a API /mod2/ com o número <numero>
    Then O resultado deve ser "<resultado>"

    Examples:
        | numero | resultado |
        | 10     | par       |
        | 7      | impar     |
        | 0      | par       |

Scenario: Verificar entrada inválida
    When Eu chamo a API /mod2/ com o texto "abc"
    Then A API deve retornar um erro 422

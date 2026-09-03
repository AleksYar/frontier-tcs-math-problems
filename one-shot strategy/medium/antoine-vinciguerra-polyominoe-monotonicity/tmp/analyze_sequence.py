#!/usr/bin/env python3
"""Exact sequence-transform diagnostics for fixed polyomino counts."""

from fractions import Fraction

A = [
    1, 1, 2, 6, 19, 63, 216, 760, 2725, 9910, 36446, 135268,
    505861, 1903890, 7204874, 27394666, 104592937, 400795844,
    1540820542, 5940738676, 22964779660, 88983512783,
    345532572678, 1344372335524, 5239988770268, 20457802016011,
    79992676367108, 313224032098244, 1228088671826973,
    4820975409710116, 18946775782611174, 74541651404935148,
    293560133910477776, 1157186142148293638, 4565553929115769162,
    18027932215016128134, 71242712815411950635, 281746550485032531911,
    1115021869572604692100, 4415695134978868448596,
    17498111172838312982542, 69381900728932743048483,
    275265412856343074274146, 1092687308874612006972082,
    4339784013643393384603906, 17244800728846724289191074,
    68557762666345165410168738, 272680844424943840614538634,
    1085035285182087705685323738, 4319331509344565487555270660,
    17201460881287871798942420736, 68530413174845561618160604928,
    273126660016519143293320026256, 1088933685559350300820095990030,
    4342997469623933155942753899000, 17326987021737904384935434351490,
    69150714562532896936574425480218, 276061302869769053815091348274853,
    1102414654388614817828362087885194,
    4403627610727810528935609181494038,
    17595360125786076902429902468975094,
    70324022977839757717649768794923974,
    281140509936541236506957176030736610,
    1124226206002101486403009097923067462,
    4496670726609716846990603851802851046,
    17990046482672581050565325516788100067,
    71990329116147598315672557624308271186,
    288146737936083547752609866746184117546,
    1153580914959613979832549218358894513290,
    4619282047583828929546825973053580643926,
    18500792645885711270652890811942343400814,
]

# Formal renewal coefficients: A(z) = 1/(1-Q(z)).
Q = [0] * len(A)
for n in range(1, len(A)):
    Q[n] = A[n] - sum(Q[k] * A[n - k] for k in range(1, n))

print("Q first 20", Q[1:21])
print("Q nonpositive", [(n, Q[n]) for n in range(1, len(Q)) if Q[n] <= 0])
print(
    "Q logconvex failures",
    [n for n in range(2, len(Q) - 1) if Q[n] ** 2 > Q[n - 1] * Q[n + 1]],
)


def determinant(matrix):
    matrix = [[Fraction(value) for value in row] for row in matrix]
    answer = Fraction(1)
    for i in range(len(matrix)):
        pivot = next((j for j in range(i, len(matrix)) if matrix[j][i]), None)
        if pivot is None:
            return 0
        if pivot != i:
            matrix[i], matrix[pivot] = matrix[pivot], matrix[i]
            answer = -answer
        value = matrix[i][i]
        answer *= value
        for j in range(i + 1, len(matrix)):
            quotient = matrix[j][i] / value
            for k in range(i, len(matrix)):
                matrix[j][k] -= quotient * matrix[i][k]
    return answer


for size in range(2, 7):
    signs = []
    for shift in range(1, min(20, len(Q) - 2 * size + 2)):
        value = determinant(
            [[Q[shift + i + j] for j in range(size)] for i in range(size)]
        )
        signs.append((shift, 1 if value > 0 else -1 if value < 0 else 0))
    print("Q Hankel signs", size, signs)
print(
    "Q/A decreasing failures",
    [n for n in range(1, len(Q) - 1) if Fraction(Q[n + 1], A[n + 1]) > Fraction(Q[n], A[n])],
)
print(
    "Q ratio tail",
    [(n, float(Fraction(Q[n + 1], Q[n]))) for n in range(len(Q) - 10, len(Q) - 1)],
)

# Curvature after removing the empirically predicted 1/n factor.
B = [n * A[n] for n in range(len(A))]
print(
    "B logconcavity failures",
    [n for n in range(2, len(B) - 1) if B[n] ** 2 < B[n - 1] * B[n + 1]],
)
print(
    "scaled B-curvature tail",
    [
        (n, float(n * n * (Fraction(B[n] ** 2, B[n - 1] * B[n + 1]) - 1)))
        for n in range(len(B) - 10, len(B) - 1)
    ],
)

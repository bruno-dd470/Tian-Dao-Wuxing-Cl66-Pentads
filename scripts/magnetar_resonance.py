import numpy as np

# 72 valeurs propres du réseau unimodulaire Γ (Nebe)
lambda_Gamma = np.array([
    0.0043740973516556257583, 0.0043740973516556258844,
    0.010995546215077851813, 0.010995546215077851848,
    0.011197776487850081092, 0.018306563103388413523,
    0.018306563103388413687, 0.029576322793137380691,
    0.037359874463993147761, 0.037359874463993147996,
    0.047227060779061605995, 0.063356180109664584017,
    0.063356180109664584215, 0.079378841213435711453,
    0.079378841213435712007, 0.095442748560291922283,
    0.11732778393430706981, 0.11732778393430706997,
    0.12970492710948967363, 0.15135542346526064350,
    0.15135542346526064357, 0.18224233526029199232,
    0.29097785324761605221, 0.29097785324761605252,
    0.30899131433464432369, 0.37392327826684409393,
    0.39492892060870845764, 0.39492892060870845765,
    0.52822943431040091584, 0.61409034101999347408,
    0.61409034101999347415, 0.75384755659699768997,
    0.80065628469062346170, 0.80065628469062346178,
    0.80089328381005198496, 1.3956134502248842121,
    1.9272159835255295502, 2.1304098745750085324,
    2.1304098745750085327, 2.2623588346586941297,
    2.5057407355677230608, 2.9765210070356088852,
    3.3535422310737084466, 3.3535422310737084469,
    3.3910324700320243714, 3.5772428437732089992,
    4.0699946798773017446, 4.0699946798773017447,
    4.3799668875911968964, 5.3111753784848464945,
    5.3111753784848464965, 6.3752579403535408666,
    8.4757579813397957892, 8.4757579813397957895,
    9.9708989763601574938, 9.9708989763601574952,
    9.9747326396419946309, 10.750743903593353286,
    10.816291213992858611, 10.816291213992858612,
    14.833876891400130416, 14.833876891400130420,
    20.899130218355758941, 22.323167047337420512,
    22.610473853320698014, 22.610473853320698025,
    35.319193889558946140, 35.319193889558946146,
    54.877918027729634123, 54.877918027729634137,
    65.647359292863189710, 65.647359292863189714
])

sqrt_vals = np.sqrt(lambda_Gamma)
n = len(sqrt_vals)
Lambda_fund = 6.132  # MeV

target = 200  # MeV (résonance observée)

print("="*70)
print("RECHERCHE DE COMBINAISONS POUR LA RÉSONANCE À 200 MeV")
print("Dans le réseau unimodulaire Γ (Nebe)")
print("="*70)

# 1. Produits λ_i × λ_j / k
print("\n1. Produits λ_i × λ_j / k")
best_error = 1.0
best_expr = None
best_val = None

for i in range(n):
    for j in range(i, n):
        for k in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 16, 20, 24, 32, 36, 48, 64, 72, 96, 128, 144]:
            val = (lambda_Gamma[i] * lambda_Gamma[j]) / k * Lambda_fund
            if 150 < val < 250:
                error = abs(val - target) / target
                if error < best_error:
                    best_error = error
                    best_expr = f"λ_{i+1} × λ_{j+1} / {k} × Λ_fund"
                    best_val = val
                    print(f"  {best_expr} = {val:.1f} MeV (erreur {error*100:.1f}%)")

# 2. |4^a √λ_i - 4^b √λ_j| × Λ_fund
print("\n2. Différences avec octaves |4^a √λ_i - 4^b √λ_j| × Λ_fund")
best_error2 = 1.0
best_expr2 = None
best_val2 = None

for a in range(0, 5):
    for b in range(a, 5):
        for i in range(n):
            for j in range(i, n):
                if a == b and i == j:
                    continue
                val = abs(4**a * sqrt_vals[i] - 4**b * sqrt_vals[j]) * Lambda_fund
                if 150 < val < 250:
                    error = abs(val - target) / target
                    if error < best_error2:
                        best_error2 = error
                        best_expr2 = f"|4^{a}√λ_{i+1} - 4^{b}√λ_{j+1}| × Λ_fund"
                        best_val2 = val
                        print(f"  {best_expr2} = {val:.1f} MeV (erreur {error*100:.1f}%)")

# 3. Sommes de √λ avec octaves
print("\n3. Sommes de √λ avec octaves |4^a √λ_i + 4^b √λ_j| × Λ_fund")
best_error3 = 1.0
best_expr3 = None
best_val3 = None

for a in range(0, 5):
    for b in range(a, 5):
        for i in range(n):
            for j in range(i, n):
                val = (4**a * sqrt_vals[i] + 4**b * sqrt_vals[j]) * Lambda_fund
                if 150 < val < 250:
                    error = abs(val - target) / target
                    if error < best_error3:
                        best_error3 = error
                        best_expr3 = f"(4^{a}√λ_{i+1} + 4^{b}√λ_{j+1}) × Λ_fund"
                        best_val3 = val
                        print(f"  {best_expr3} = {val:.1f} MeV (erreur {error*100:.1f}%)")

# 4. Triplets de √λ
print("\n4. Triplets de √λ (somme) × Λ_fund")
best_error4 = 1.0
best_expr4 = None
best_val4 = None

for i in range(n):
    for j in range(i+1, n):
        for k in range(j+1, n):
            val = (sqrt_vals[i] + sqrt_vals[j] + sqrt_vals[k]) * Lambda_fund
            if 150 < val < 250:
                error = abs(val - target) / target
                if error < best_error4:
                    best_error4 = error
                    best_expr4 = f"(√λ_{i+1} + √λ_{j+1} + √λ_{k+1}) × Λ_fund"
                    best_val4 = val
                    print(f"  {best_expr4} = {val:.1f} MeV (erreur {error*100:.1f}%)")

print("\n" + "="*70)
print("MEILLEURES APPROXIMATIONS")
print("="*70)
if best_expr:
    print(f"Produit : {best_expr} = {best_val:.1f} MeV (erreur {best_error*100:.1f}%)")
if best_expr2:
    print(f"Différence avec octaves : {best_expr2} = {best_val2:.1f} MeV (erreur {best_error2*100:.1f}%)")
if best_expr3:
    print(f"Somme avec octaves : {best_expr3} = {best_val3:.1f} MeV (erreur {best_error3*100:.1f}%)")
if best_expr4:
    print(f"Triplet : {best_expr4} = {best_val4:.1f} MeV (erreur {best_error4*100:.1f}%)")
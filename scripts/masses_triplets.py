import numpy as np
from scipy.linalg import eigh
from scipy.optimize import minimize

# ============================================================
# VALEURS PROPRES DE Λ72 (24 distinctes, multiplicité 3)
# ============================================================
lambda_vals = np.array([
    0.005598888244, 0.014788161397, 0.023613530390, 0.047721374280,
    0.064852463555, 0.091121167630, 0.154495657167, 0.186961639133,
    0.264114717155, 0.376923778298, 0.400446641905, 0.697806725112,
    0.963607991763, 1.131179417329, 1.252870367784, 1.488260503518,
    1.695516235016, 1.788621421887, 2.189983443796, 3.187628970177,
    4.987366319821, 5.375371951797, 10.449565109178, 11.161583523669
])

# ============================================================
# ASSOCIATION PENTADE -> VALEUR PROPRE (12 premières λ)
# ============================================================
pentade_lambda = {
    "P1": lambda_vals[0],
    "P2": lambda_vals[1],
    "P3": lambda_vals[2],
    "P4": lambda_vals[3],
    "P5": lambda_vals[4],
    "P6": lambda_vals[5],
    "N1": lambda_vals[6],
    "N2": lambda_vals[7],
    "N3": lambda_vals[8],
    "N4": lambda_vals[9],
    "N5": lambda_vals[10],
    "N6": lambda_vals[11]
}

# ============================================================
# LISTE DES 20 TRIPLETS (Merkabah)
# ============================================================
triplets = [
    ["P1","P2","P4"],   # 1: 3P
    ["P1","P3","P5"],   # 2: 3P
    ["P2","P3","P6"],   # 3: 3P
    ["P4","P5","N2"],   # 4: 2P+1N
    ["P5","P6","N3"],   # 5: 2P+1N
    ["P1","P6","N4"],   # 6: 2P+1N
    ["P2","P5","N6"],   # 7: 2P+1N
    ["P3","P4","N6"],   # 8: 2P+1N
    ["P1","N2","N6"],   # 9: 1P+2N
    ["P1","N3","N5"],   # 10: 1P+2N
    ["P2","N3","N5"],   # 11: 1P+2N
    ["P3","N2","N4"],   # 12: 1P+2N
    ["P4","N1","N3"],   # 13: 1P+2N
    ["P4","N5","N6"],   # 14: 1P+2N
    ["P5","N1","N4"],   # 15: 1P+2N
    ["P6","N1","N2"],   # 16: 1P+2N
    ["P2","N1","N4"],   # 17: 1P+2N
    ["P3","N1","N5"],   # 18: 1P+2N
    ["P6","N5","N6"],   # 19: 1P+2N
    ["N2","N3","N4"]    # 20: 3N
]

# ============================================================
# CALCUL DE LA MASSE D'UN TRIPLET
# ============================================================
def triplet_mass(triplet, pentade_lambda, a, b):
    """m = a * Σ√λ + b * Σλ"""
    sqrt_sum = np.sum([np.sqrt(pentade_lambda[p]) for p in triplet])
    lambda_sum = np.sum([pentade_lambda[p] for p in triplet])
    return a * sqrt_sum + b * lambda_sum

# ============================================================
# CONSTRUCTION DE LA MATRICE T (20x20)
# ============================================================
def build_T(a, b, coupling_strength=0.1):
    n = len(triplets)
    T = np.zeros((n, n))
    # Diagonale : masse du triplet
    for i in range(n):
        T[i, i] = triplet_mass(triplets[i], pentade_lambda, a, b)
    # Couplages : si deux triplets partagent une pentade
    for i in range(n):
        for j in range(i+1, n):
            if set(triplets[i]) & set(triplets[j]):
                dist = abs(T[i, i] - T[j, j])
                if dist > 1e-12:
                    T[i, j] = coupling_strength / dist
                    T[j, i] = T[i, j]
    return T

# ============================================================
# OPTIMISATION DES PARAMÈTRES a, b (sur quelques triplets)
# ============================================================
# Masses expérimentales (MeV) pour les premiers triplets (hadrons légers)
# Triplet 1 (3P) -> pion (135), triplet 2 -> kaon (494), triplet 3 -> proton (938)
masses_exp = [135.0, 493.7, 938.3]

def error(params):
    a, b = params
    mass_pred = []
    for i in range(len(masses_exp)):
        mass_pred.append(triplet_mass(triplets[i], pentade_lambda, a, b))
    return np.sum((np.array(mass_pred) - np.array(masses_exp))**2)

# Optimisation
res = minimize(error, [1.0, 0.0], method='Nelder-Mead', options={'maxiter': 5000})
a_opt, b_opt = res.x

print("="*60)
print("PARAMÈTRES OPTIMISÉS")
print("="*60)
print(f"a = {a_opt:.3f}")
print(f"b = {b_opt:.3f}")

# ============================================================
# DIAGONALISATION DE T AVEC LES PARAMÈTRES OPTIMISÉS
# ============================================================
T_mat_opt = build_T(a_opt, b_opt, coupling_strength=0.1)
eigvals, _ = eigh(T_mat_opt)
eigvals = np.sort(eigvals)

print("\n" + "="*60)
print("VALEURS PROPRES DE T (masses prédites, MeV)")
print("="*60)
for i, val in enumerate(eigvals):
    print(f"{i+1:2d}: {val:.1f} MeV")

# ============================================================
# COMPARAISON AVEC LES MASSES EXPÉRIMENTALES
# ============================================================
print("\n" + "="*60)
print("COMPARAISON AVEC LES HADRONS LÉGERS")
print("="*60)
print(f"Triplet 1 (3P) -> pion      : {triplet_mass(triplets[0], pentade_lambda, a_opt, b_opt):.1f} MeV (exp: 135.0)")
print(f"Triplet 2 (3P) -> kaon      : {triplet_mass(triplets[1], pentade_lambda, a_opt, b_opt):.1f} MeV (exp: 493.7)")
print(f"Triplet 3 (3P) -> proton    : {triplet_mass(triplets[2], pentade_lambda, a_opt, b_opt):.1f} MeV (exp: 938.3)")

print("\n" + "="*60)
print("AUTRES MASSES PRÉDITES (MeV)")
print("="*60)
for i in range(len(triplets)):
    m = triplet_mass(triplets[i], pentade_lambda, a_opt, b_opt)
    polarite = ""
    if "P" in triplets[i][0] and "P" in triplets[i][1] and "P" in triplets[i][2]:
        polarite = "3P"
    elif "N" in triplets[i][0] and "N" in triplets[i][1] and "N" in triplets[i][2]:
        polarite = "3N"
    elif sum([1 for p in triplets[i] if "P" in p]) == 2:
        polarite = "2P+1N"
    else:
        polarite = "1P+2N"
    print(f"Triplet {i+1:2d} ({polarite}): m = {m:.1f} MeV")
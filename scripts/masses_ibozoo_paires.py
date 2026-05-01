import numpy as np

# ============================================================
# VALEURS PROPRES DE Λ72 (24 distinctes)
# ============================================================
lambda_vals = np.array([
    0.005598888244, 0.014788161397, 0.023613530390, 0.047721374280,
    0.064852463555, 0.091121167630, 0.154495657167, 0.186961639133,
    0.264114717155, 0.376923778298, 0.400446641905, 0.697806725112,
    0.963607991763, 1.131179417329, 1.252870367784, 1.488260503518,
    1.695516235016, 1.788621421887, 2.189983443796, 3.187628970177,
    4.987366319821, 5.375371951797, 10.449565109178, 11.161583523669
])

# Racines carrées
sqrt_vals = np.sqrt(lambda_vals)

# ============================================================
# MASSES EXPÉRIMENTALES (MeV)
# ============================================================
masses_exp = {
    "e": 0.511,
    "mu": 105.7,
    "pi": 135.0,
    "K": 493.7,
    "p": 938.3,
    "J/psi": 3097,
    "Upsilon": 9460,
    "W": 80370,
    "Z": 91190,
    "H": 125000
}

# ============================================================
# HYPOTHÈSE : m = C * |√λ_i - √λ_j|
# Calibration sur une particule (pion)
# ============================================================
# On prend la plus petite différence non nulle comme candidat pour le pion
differences = []
for i in range(len(sqrt_vals)):
    for j in range(i+1, len(sqrt_vals)):
        diff = abs(sqrt_vals[i] - sqrt_vals[j])
        differences.append((diff, i, j))

differences.sort(key=lambda x: x[0])

# Calibration sur le pion (135.0 MeV) avec la première différence
# (on pourrait aussi prendre la moyenne des 2-3 plus petites)
best_diff_pion = differences[0][0]  # plus petite différence
C = 135.0 / best_diff_pion

print("="*60)
print("HYPOTHÈSE : m = C * |√λ_i - √λ_j|")
print("Calibration sur le pion (135.0 MeV)")
print(f"Plus petite différence : {best_diff_pion:.6f}")
print(f"C = {C:.2f} MeV")
print("="*60)

# ============================================================
# LISTE DES MASSES PRÉDITES
# ============================================================
print("\nMasses prédites (MeV) par différence |√λ_i - √λ_j| :")
print("Index i  j  | diff   | m_pred   | Particule candidate")
print("-"*50)

candidates = []
for diff, i, j in differences[:20]:  # afficher les 20 plus petites
    m_pred = C * diff
    candidates.append((m_pred, i, j, diff))
    print(f"{i+1:2d}  {j+1:2d}   {diff:.6f}  {m_pred:8.1f}   ")

# ============================================================
# COMPARAISON AVEC LES MASSES EXPÉRIMENTALES
# ============================================================
print("\n" + "="*60)
print("COMPARAISON AVEC LES PARTICULES CONNUES")
print("="*60)

# On associe chaque particule à la différence la plus proche
for nom, m_exp in masses_exp.items():
    # Trouver la différence la plus proche de m_exp/C
    target_diff = m_exp / C
    best_i, best_j = -1, -1
    best_diff = None
    best_dist = float('inf')
    for diff, i, j in differences:
        dist = abs(diff - target_diff)
        if dist < best_dist:
            best_dist = dist
            best_diff = diff
            best_i, best_j = i, j
    m_pred = C * best_diff
    ratio = m_pred / m_exp
    print(f"{nom:8s} : m_pred = {m_pred:8.1f} MeV (exp: {m_exp:8.1f})  ratio = {ratio:.3f}  (λ{best_i+1}, λ{best_j+1})")
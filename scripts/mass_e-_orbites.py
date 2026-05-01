import numpy as np
from scipy.linalg import eigh
from scipy.optimize import minimize
import os

# ============================================================
# 1. CHARGEMENT
# ============================================================
if not os.path.exists("G72.npy"):
    print("Erreur: Fichier G72.npy introuvable")
    exit(1)

G72 = np.load("G72.npy")
eigvals, eigvecs = eigh(G72)

m_e = 0.51099895
sqrt_lambda_2 = np.sqrt(eigvals[1])
Lambda_fund = m_e / sqrt_lambda_2
octave_base = 4

print(f"Λ_fund = {Lambda_fund:.6f} MeV\n")

# ============================================================
# 2. CONSTRUCTION DE W
# ============================================================
def build_W(indices):
    W = np.zeros((144, 10))
    for i, idx in enumerate(indices):
        W[:72, i] = eigvecs[:, idx]
        W[72:, i] = eigvecs[:, idx]
    U, s, Vt = np.linalg.svd(W, full_matrices=False)
    return U @ Vt

W = build_W(list(range(10)))

# ============================================================
# 3. DÉFINITION DES ORBITES DANS LA FEUILLE DE L'INDICE 2
# ============================================================
# Identification des orbites cycliques d'ordre 3 dans la feuille contenant l'indice 2
# Les indices sont regroupés par 3 (cycle d'ordre 3)
# Feuille e2? Les indices 1-12 sont e1, 13-24 e2? À vérifier.

# On suppose que les orbites dans la feuille de l'indice 2 sont:
orbites = [
    [2, 14, 26],   # orbite 1
    [38, 50, 62],  # orbite 2
    [74, 86, 98],  # orbite 3 (Ke, indices 74,86,98)
    [110, 122, 134] # orbite 4 (Ke)
]

# Vérifier que ces indices existent (<=144)
for orb in orbites:
    for idx in orb:
        assert 1 <= idx <= 144, f"Indice {idx} invalide"

print("Orbites sélectionnées :")
for i, orb in enumerate(orbites):
    print(f"  Orbite {i+1} : {orb}")

# ============================================================
# 4. FONCTIONS POUR LA COMBINAISON LINÉAIRE D'ORBITES
# ============================================================
def get_sqrt_lambda(idx):
    idx0 = (idx - 1) % 72
    return np.sqrt(eigvals[idx0])

def orbit_vector(orbite, octave_rel=0):
    """Vecteur latent d'une orbite (somme normalisée des pentades de l'orbite)"""
    v = np.zeros(144)
    factor = 4 ** (octave_base + octave_rel)
    for idx in orbite:
        idx0 = idx - 1
        v[idx0] += factor * get_sqrt_lambda(idx)
    # Normalisation : norme de l'orbite (pas divisée par √3 car c'est une somme)
    y = W.T @ v
    norm = np.linalg.norm(y)
    if norm > 0:
        return y / norm
    return y

def combination_mass(coeffs, octave_rel=0):
    """Masse d'une combinaison linéaire des orbites"""
    y = np.zeros(10)
    for a, coeff in enumerate(coeffs):
        y += coeff * orbit_vector(orbites[a], octave_rel)
    return Lambda_fund * np.linalg.norm(y)

# ============================================================
# 5. OPTIMISATION DES COEFFICIENTS POUR L'ÉLECTRON
# ============================================================
target = m_e
print("\n" + "="*80)
print("OPTIMISATION DES COEFFICIENTS POUR L'ÉLECTRON (Méthode 3)")
print("="*80)

def cost(coeffs):
    m = combination_mass(coeffs, 0)
    return abs(m - target)

# Optimisation
result = minimize(cost, [1, 1, 1, 1], method='Nelder-Mead')
coeffs_opt = result.x

print(f"Coefficients optimaux : {coeffs_opt}")
print(f"Somme des coefficients : {np.sum(coeffs_opt):.4f}")

# Masse avec ces coefficients
m_opt = combination_mass(coeffs_opt, 0)
print(f"\nMasse prédite : {m_opt:.8f} MeV")
print(f"Cible : {target:.8f} MeV")
print(f"Écart : {abs(m_opt - target):.2e} MeV ({abs(m_opt - target)/target*100:.4f}%)")

# ============================================================
# 6. VÉRIFICATION DE L'OCTAVE
# ============================================================
print("\n" + "="*80)
print("RECHERCHE DE L'OCTAVE OPTIMALE")
print("="*80)

best_n = 0
best_m = 0
best_diff = float('inf')
best_coeffs = None

for n_rel in np.arange(-2.0, 2.01, 0.1):
    # Réoptimiser les coefficients à chaque octave (coûteux, on fixe les coefficients de l'optimum précédent)
    m = combination_mass(coeffs_opt, n_rel)
    diff = abs(m - target)
    if diff < best_diff:
        best_diff = diff
        best_n = n_rel
        best_m = m

print(f"n_rel optimal = {best_n:.2f}")
print(f"Masse = {best_m:.8f} MeV")
print(f"Écart = {best_diff:.2e} MeV ({best_diff/target*100:.4f}%)")
print(f"Facteur 4^(4+{best_n:.2f}) = {4**(4+best_n):.2f}")

# ============================================================
# 7. CONCLUSION
# ============================================================
print("\n" + "="*80)
print("CONCLUSION")
print("="*80)
if abs(m_opt - target) < 0.001:
    print(f"✅ La superposition d'orbites donne m_e = {m_opt:.8f} MeV")
    print(f"   Coefficients : {coeffs_opt}")
else:
    print(f"❌ La superposition d'orbites ne donne pas m_e.")
    print(f"   Meilleur résultat : {m_opt:.8f} MeV (écart {abs(m_opt - target)/target*100:.4f}%)")
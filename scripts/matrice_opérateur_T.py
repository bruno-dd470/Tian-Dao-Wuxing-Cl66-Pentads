import numpy as np
from scipy.linalg import eigh
from itertools import combinations

# ============================================================
# 1. CHARGEMENT
# ============================================================
G72 = np.load("G72.npy")
eigvals, eigvecs = eigh(G72)

m_e = 0.51099895
sqrt_lambda_2 = np.sqrt(eigvals[1])
Lambda_fund = m_e / sqrt_lambda_2
octave_base = 6

def build_W(indices):
    W = np.zeros((144, 10))
    for i, idx in enumerate(indices):
        W[:72, i] = eigvecs[:, idx]
        W[72:, i] = eigvecs[:, idx]
    U, s, Vt = np.linalg.svd(W, full_matrices=False)
    return U @ Vt

W = build_W(list(range(10)))

# ============================================================
# 2. FONCTIONS POUR UN TRIPLET (MERKABAH)
# ============================================================
def pentad_latent(idx):
    v = np.zeros(144)
    factor = 4 ** octave_base
    idx0 = (idx - 1) % 72
    v[idx-1] = factor * np.sqrt(eigvals[idx0])
    return W.T @ v

def triplet_latent(idx1, idx2, idx3, signes=(1,1,1)):
    return (signes[0] * pentad_latent(idx1) +
            signes[1] * pentad_latent(idx2) +
            signes[2] * pentad_latent(idx3))

def triplet_mass(idx1, idx2, idx3, signes=(1,1,1)):
    return Lambda_fund * np.linalg.norm(triplet_latent(idx1, idx2, idx3, signes))

# ============================================================
# 3. SÉLECTION DES TRIPLETS DANS LA FENÊTRE 80-130 GeV
# ============================================================
print("Recherche des triplets (Merkabah) dans la fenêtre 80-130 GeV...")
target_range = (80000, 130000)

triplet_list = []
triplet_masses_list = []

# Parcours limité aux indices 1-72 (pentades Sheng)
indices = list(range(1, 73))

# On explore les combinaisons de 3 indices (C(72,3) = 58905, c'est raisonnable)
for i, j, k in combinations(indices, 3):
    # Essayer différentes combinaisons de signes
    for signes in [(1,1,1), (1,1,-1), (1,-1,-1), (1,-1,1)]:
        m = triplet_mass(i, j, k, signes)
        if target_range[0] < m < target_range[1]:
            triplet_list.append((i, j, k, signes))
            triplet_masses_list.append(m)
            if len(triplet_list) >= 30:  # Limite pour ne pas trop charger
                break
    if len(triplet_list) >= 30:
        break

n_triplets = len(triplet_list)
print(f"Nombre de triplets sélectionnés : {n_triplets}")

if n_triplets == 0:
    print("Aucun triplet trouvé. Élargissez la fenêtre.")
    exit()

# ============================================================
# 4. MATRICE DES CHEVAUCHEMENTS NORMALISÉS
# ============================================================
print("Construction de la matrice de chevauchement...")
S = np.zeros((n_triplets, n_triplets))

for i in range(n_triplets):
    i1, i2, i3, sgn_i = triplet_list[i]
    v_i = triplet_latent(i1, i2, i3, sgn_i)
    norm_i = np.linalg.norm(v_i)
    if norm_i > 0:
        v_i = v_i / norm_i
    else:
        v_i = np.zeros_like(v_i)
    
    for j in range(i, n_triplets):
        j1, j2, j3, sgn_j = triplet_list[j]
        v_j = triplet_latent(j1, j2, j3, sgn_j)
        norm_j = np.linalg.norm(v_j)
        if norm_j > 0:
            v_j = v_j / norm_j
        else:
            v_j = np.zeros_like(v_j)
        
        S[i, j] = abs(np.dot(v_i, v_j))
        S[j, i] = S[i, j]

# ============================================================
# 5. CALIBRATION SUR W (on prend la plus grande valeur propre)
# ============================================================
eigvals_S, _ = eigh(S)
eigvals_S_sorted = np.sort(eigvals_S)[::-1]

target_W = 80379
alpha = target_W / eigvals_S_sorted[0] if eigvals_S_sorted[0] > 0 else 1

M = alpha * S
eigvals_M, _ = eigh(M)
eigvals_M_sorted = np.sort(eigvals_M)[::-1]

print("\nMasses propres (MeV) :")
for i in range(min(10, len(eigvals_M_sorted))):
    print(f"  λ{i+1} = {eigvals_M_sorted[i]:.0f} MeV")

# ============================================================
# 6. COMPARAISON AVEC W, Z, H
# ============================================================
targets = {"W": 80379, "Z": 91188, "H": 125250}
print("\nComparaison avec les bosons :")
for name, target in targets.items():
    if len(eigvals_M_sorted) == 0:
        continue
    idx = np.argmin(np.abs(eigvals_M_sorted - target))
    closest = eigvals_M_sorted[idx]
    err = abs(closest - target) / target * 100
    print(f"  {name}: prédit {closest:.0f} MeV (exp {target} MeV) — erreur {err:.1f}%")
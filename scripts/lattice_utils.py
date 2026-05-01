"""Utilities for Λ₇₂ lattice operations."""
import numpy as np

def load_lattice_data(path="."):
    G72 = np.load(f"{path}/G72.npy")
    eigvals = np.loadtxt(f"{path}/eigvals_72.txt")
    eigvecs = np.load(f"{path}/eigvecs_72.npy")
    return G72, eigvals, eigvecs

def build_W(eigvecs, indices=range(10), dim=144):
    W_raw = np.zeros((dim, len(indices)))
    for i, idx in enumerate(indices):
        W_raw[:72, i] = eigvecs[:, idx]
        W_raw[72:, i] = eigvecs[:, idx]
    U, s, Vt = np.linalg.svd(W_raw, full_matrices=False)
    return U @ Vt

def activation_vector(indices, octaves, signs, eigvals, base_octave=4):
    v = np.zeros(144)
    for idx, n_rel, sgn in zip(indices, octaves, signs):
        factor = 4 ** (base_octave + n_rel)
        eig_idx = idx % 72
        v[idx] = sgn * factor * np.sqrt(eigvals[eig_idx])
    return v

def latent_mass(v, W, Lambda_fund):
    return Lambda_fund * np.linalg.norm(W.T @ v)

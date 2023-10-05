#!/usr/bin/env python3
"""Generate k-points and sample band paths."""
import numpy as np
from scipy.linalg import norm, pinv

from .data import SPECIAL_POINTS
from .logger import log


def kpoint_convert(k_points, lattice_vectors):
    """Convert scaled k-points to cartesian coordinates.

    Reference: https://gitlab.com/ase/ase/-/blob/master/ase/dft/kpoints.py

    Args:
        k_points (ndarray): k-points.
        lattice_vectors (ndarray): Lattice vectors.

    Returns:
        ndarray: k-points in cartesian coordinates.
    """
    inv_cell = 2 * np.pi * pinv(lattice_vectors).T
    return k_points @ inv_cell


def monkhorst_pack(nk, lattice_vectors):
    """Generate a Monkhorst-Pack mesh of k-points, i.e., equally spaced k-points.

    Args:
        nk (list | tuple | ndarray): Number of k-points per axis.
        lattice_vectors (ndarray): Lattice vectors.

    Returns:
        tuple[ndarray, ndarray]: k-points and their respective weights.
    """
    # Same index matrix as in Atoms._get_index_matrices()
    nktotal = np.prod(nk)
    ms = np.arange(nktotal)
    m1 = np.floor(ms / (nk[2] * nk[1])) % nk[0]
    m2 = np.floor(ms / nk[2]) % nk[1]
    m3 = ms % nk[2]
    M = np.column_stack((m1, m2, m3))

    k_points = (M + 0.5) / nk - 0.5
    # Without removing redundancies the weight is the same for all k-points
    return kpoint_convert(k_points, lattice_vectors), np.ones(nktotal) / nktotal


def bandpath(lattice, lattice_vectors, path, N):
    """Generate sampled band paths.

    Args:
        lattice (str): Lattice type.
        lattice_vectors (ndarray): Lattice vectors.
        path (str): Bandpath.
        N (int): Number of sampling points.

    Returns:
        ndarray: Sampled k-points.
    """
    # Convert path to a list and get special points
    path_list = list(path.upper())
    s_points = SPECIAL_POINTS[lattice]
    # Commas indicate jumps and are no special points
    N_special = len([p for p in path_list if p != ','])

    # Input handling
    if N_special > N:
        log.warning('Sampling is smaler than the number of special points.')
        N = N_special
    for p in path_list:
        if p not in (*s_points, ','):
            raise KeyError(f'{p} is not a special point for the {lattice} lattice.')

    # Calculate distances between special points
    dists = []
    for i in range(len(path_list) - 1):
        if ',' not in path_list[i:i + 2]:
            # Use subtract since s_points are lists
            dist = np.subtract(s_points[path_list[i + 1]], s_points[path_list[i]])
            dists.append(norm(kpoint_convert(dist, lattice_vectors)))
        else:
            # Set distance to zero when jumping between special points
            dists.append(0)

    # Calculate sample points between the special points
    scaled_dists = (N - N_special) * np.array(dists) / sum(dists)
    samplings = np.int64(np.round(scaled_dists))

    # If our sampling does not match the given N add the difference to the longest distance
    if N - N_special - np.sum(samplings) != 0:
        samplings[np.argmax(samplings)] += N - N_special - np.sum(samplings)

    # Generate k-point coordinates
    k_points = [s_points[path_list[0]]]  # Insert the first special point
    for i in range(len(path_list) - 1):
        # Only do something when not jumping between special points
        if ',' not in path_list[i:i + 2]:
            s_start = s_points[path_list[i]]
            s_end = s_points[path_list[i + 1]]
            # Get the vector between special points
            k_dist = np.subtract(s_end, s_start)
            # Add scaled vectors to the special point to get the new k-points
            k_points += [s_start + k_dist * (n + 1) / (samplings[i] + 1)
                         for n in range(samplings[i])]
            # Append the special point we are ending at
            k_points.append(s_end)
        # If we jump, add the new special point to start from
        elif path_list[i] == ',':
            k_points.append(s_points[path_list[i + 1]])
    return np.asarray(k_points)


def kpoints2axis(lattice, lattice_vectors, path, k_points):
    """Generate the x-axis for band structures from k-points and the respective band path.

    Args:
        lattice (str): Lattice type.
        lattice_vectors (ndarray): Lattice vectors.
        path (str): Bandpath.
        k_points (ndarray): k-points.

    Returns:
        tuple[ndarray, ndarray, list]: k-point axis, special point coordinates, and labels.
    """
    # Convert path to a list and get the special points
    path_list = list(path.upper())
    s_points = SPECIAL_POINTS[lattice]

    # Calculate the distances between k-points
    k_dist = k_points[1:] - k_points[:-1]
    dists = norm(kpoint_convert(k_dist, lattice_vectors), axis=1)

    # Create the labels
    labels = []
    for i in range(len(path_list)):
        # If a jump happened before the current step the special point is already included
        if i > 1 and path_list[i - 1] == ',':
            continue
        # Append the special point if no jump happens
        if ',' not in path_list[i:i + 2]:
            labels.append(path_list[i])
        # When jumping join the special points to one label
        elif path_list[i] == ',':
            labels.append(''.join(path_list[i - 1:i + 2]))

    # Get the indices of the special points
    special_indices = [0]  # The first special point is trivial
    for p in labels[1:]:
        # Only search the k-points starting from the previous special point
        shift = special_indices[-1]
        k = k_points[shift:]
        # We index p[0] since p could be a joined label of a jump
        # This expression simply finds the special point in the k_points matrix
        index = np.flatnonzero((k == s_points[p[0]]).all(axis=1))[0] + shift
        special_indices.append(index)
        # Set the distance between special points to zero if we have a jump
        if ',' in p:
            dists[index] = 0

    # Insert a zero at the beginning and add up the lengths to create the k-axis
    k_axis = np.append([0], np.cumsum(dists))
    return k_axis, k_axis[special_indices], labels

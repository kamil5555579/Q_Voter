from voter import VoterModel
import numpy as np
import matplotlib.pyplot as plt
from typing import Sequence
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

def run_one_p(N, q, p, M, c, p_idx):
    v = VoterModel(N, q, p, M, c)
    v.run_simulation()
    last_values = int(M/20)
    c_last_values = v.c_values[-last_values:]
    m_last_values = np.abs(2 * c_last_values - 1)
    m = np.mean(m_last_values)
    return p_idx, m

def run_one_R(N, q, p, M, c, R_idx):
    v = VoterModel(N, q, p, M, c)
    v.run_simulation()
    c = v.get_final_concentration()
    m = np.abs(2 * c - 1)
    print(R_idx, p)
    return R_idx, m
            

def analyze_parameter_p(p: Sequence[float], N: int, q: int, M: int, c: float, R: int, with_polarization: bool = False) -> None:
    """
    Analyzes the parameter p
    :param p: Array of p values
    :param N: Number of voters
    :param q: Size of lobby
    :param M: Number of Monte Carlo steps
    :param c: Initial concentration of 1s
    :param R: Number of repetitions for each p value
    :param with_polarization: Compare polarized intialization with random initialization
    """

    mean_magnetization_values = np.zeros(len(p))

    for idx, p_value in enumerate(p):

        magnetization_values = np.zeros(R)

        with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
            futures = [executor.submit(run_one_R, N, q, p_value, M, c, R_idx) for R_idx in range(R)]
            for future in as_completed(futures):
                R_idx, m = future.result()
                magnetization_values[R_idx] = m
        
        mean_magnetization_values[idx] = np.mean(magnetization_values)

    plt.plot(p, mean_magnetization_values, label='random initialization')
    plt.xlabel("p")
    plt.ylabel("|m|")
    plt.title(f"Magnetization over p (N={N}, q={q}, M={M})")

    if with_polarization: # do the same with polarization/concentration equal to 1

        mean_magnetization_values = np.zeros(len(p))

        for idx, p_value in enumerate(p):

            magnetization_values = np.zeros(R)

            with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
                futures = [executor.submit(run_one_R, N, q, p_value, M, 1, R_idx) for R_idx in range(R)]
                for future in as_completed(futures):
                    R_idx, m = future.result()
                    magnetization_values[R_idx] = m
            
            mean_magnetization_values[idx] = np.mean(magnetization_values)

        plt.plot(p, mean_magnetization_values, label='polarized initialization')
        plt.legend()

    plt.savefig('results/magnetization_p{}{}.png'.format(q, N))

def analyze_parameter_p_from_single_run(p: Sequence[float], N: int, q: int, M: int, c: float, with_polarization: bool = False) -> None:
    """
    Analyzes the parameter p
    :param p: Array of p values
    :param N: Number of voters
    :param q: Size of lobby
    :param M: Number of Monte Carlo steps
    :param c: Initial concentration of 1s
    :param with_polarization: Compare polarized intialization with random initialization
    """

    mean_magnetization_values = np.zeros(len(p))

    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        futures = [executor.submit(run_one_p, N, q, p_value, M, c, idx) for idx, p_value in enumerate(p)]
        for future in as_completed(futures):
            p_idx, m = future.result()
            mean_magnetization_values[p_idx] = m

    plt.plot(p, mean_magnetization_values, '-o', label='random initialization')
    plt.xlabel("p")
    plt.ylabel("|m|")
    plt.title(f"Magnetization over p (N={N}, q={q}, M={M})")

    if with_polarization: # do the same with polarization/concentration equal to 1

        mean_magnetization_values = np.zeros(len(p))

        with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
            futures = [executor.submit(run_one_p, N, q, p_value, M, 1, idx) for idx, p_value in enumerate(p)]
            for future in as_completed(futures):
                p_idx, m = future.result()
                mean_magnetization_values[p_idx] = m

        plt.plot(p, mean_magnetization_values, '-o', label='polarized initialization')
        plt.legend()

    plt.savefig('results/single_run_magnetization_p{}{}.png'.format(q, N))
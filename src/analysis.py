from voter import VoterModel
import numpy as np
import matplotlib.pyplot as plt
from typing import Sequence
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

def run_once(N, q, p, M, c, R_idx):
    v = VoterModel(N, q, p, M, c)
    v.run_simulation()
    c = v.get_final_concentration()
    m = np.abs(2 * c - 1)
    print(R_idx, p)
    return R_idx, m
            


def analyze_parameter_p(p: Sequence[float], N: int, q: int, M: int, c: float, R: int) -> None:
    """
    Analyzes the parameter p
    :param p: Array of p values
    :param N: Number of voters
    :param q: Size of lobby
    :param M: Number of Monte Carlo steps
    :param c: Initial concentration of 1s
    :param R: Number of repetitions for each p value
    """

    mean_magnetization_values = np.zeros(len(p))

    for idx, p_value in enumerate(p):

        magnetization_values = np.zeros(R)

        with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
            futures = [executor.submit(run_once, N, q, p_value, M, c, R_idx) for R_idx in range(R)]
            for future in as_completed(futures):
                R_idx, m = future.result()
                magnetization_values[R_idx] = m
        
        mean_magnetization_values[idx] = np.mean(magnetization_values)

    plt.plot(p, mean_magnetization_values)
    plt.xlabel("p")
    plt.ylabel("|m|")
    plt.title(f"Magnetization over p (N={N}, q={q}, M={M})")
    plt.savefig('results/magnetization_p{}{}.png'.format(q, N))


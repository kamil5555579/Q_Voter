import voter
import analysis
import numpy as np

def main():
    # v = voter.VoterModel(50, 7, 0.09, 500, 1)
    # v.run_simulation()
    # v.draw_concentration()
    #v.animate_voters_evolution()
    p_values = np.arange(0.05, 0.25, 0.005)
    p_values = np.linspace(0, 0.6, 32)
    analysis.analyze_parameter_p_from_single_run(p_values, 500, 3, 1000, 0.5, False)

if __name__ == "__main__":
    main()

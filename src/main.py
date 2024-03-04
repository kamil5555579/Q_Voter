import voter
import analysis
import numpy as np

def main():
    v = voter.VoterModel(10, 7, 0.09, 100, 0.5)
    v.run_simulation()
    v.draw_concentration()
    v.animate_voters_evolution()
    # p_values = np.arange(0.1, 0.2, 0.002)
    # analysis.analyze_parameter_p(p_values, 50, 6, 500, 0.5, 16, True)

if __name__ == "__main__":
    main()

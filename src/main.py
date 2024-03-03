import voter
import analysis
import numpy as np

def main():
    # v = voter.VoterModel(100, 7, 0.09, 1000, 0.5)
    # v.run_simulation()
    # v.draw_concentration()
    p_values = np.arange(0.075, 0.105, 0.001)
    analysis.analyze_parameter_p(p_values, 100, 8, 500, 0.5, 50)

if __name__ == "__main__":
    main()

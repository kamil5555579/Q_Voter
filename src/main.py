import voter

def main():
    # Create a voter object
    v = voter.VoterModel(100, 8, 0.09, 1000, 0.5)
    # Run the simulation
    v.run_simulation()
    # Draw the concentration
    v.draw_concentration()

if __name__ == "__main__":
    main()

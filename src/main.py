import voter

def main():
    # Create a voter object
    v = voter.VoterModel(100, 10, 0.5, 1000)
    # Run the simulation
    v.run_simulation()

if __name__ == "__main__":
    main()

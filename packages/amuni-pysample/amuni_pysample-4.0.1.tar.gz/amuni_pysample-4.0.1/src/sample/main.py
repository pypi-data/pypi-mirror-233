from sample import amuni

# This import above actually executes the code in amuni.py mainline
# (not the code within sample functions)


def main():
    print("***Running main within sample")
    amuni.add_one(1)
    print("***And back in main within sample")


if __name__ == "__main__":
    # This block of code will only run if main.py is executed directly
    main()

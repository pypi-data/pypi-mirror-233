import pythoness

@pythoness.spec("Given n, a number of letters, and ending, a string of letters, return all English words that are n-letters long and end with the string given by ending.",
                # tests = ["enders(11,'orange') == ['pseudorange']"],
                verbose = True)
def enders(n : int, ending: str) -> [str]:
    ""

print(enders(11, "orange"))
print(enders(11, "range"))


import __main__ as main
def is_interactive():
    if not hasattr(main, '__file__'):
        # executed interactively (e.g. at the CLI or in a Jupyter notebook)                                           
        return True
    else:
        # executed non-interactively (executing a script)                                                             
        return False

print("WUT")
print(is_interactive())

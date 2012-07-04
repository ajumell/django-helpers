samples = []

samples.append("""
 aju : "one",
 two : "two",
""")


def main():
    output = samples[0].strip()
    if output[-1:] == ',':
        output = output[:-1]
    print output

if __name__ == "__main__":
    main()
import re
import sys


def main():
    file = "/Users/pkorir/Downloads/sta_examples/relion3/extract3d_particles.star"
    with open(file, 'r') as f:
        data = f.read()

    # now we get all blocks
    for match in re.finditer(r"\ndata_(.*)\n", data, re.MULTILINE | re.DOTALL):
        print(match, match.start(), match.end())
        result = re.search(r"(.*)\ndata_.*\n", data[match.start():], re.MULTILINE | re.DOTALL)
        print(result)
    return 0


if __name__ == '__main__':
    sys.exit(main())

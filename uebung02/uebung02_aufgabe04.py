def calculate_h_index(citations):
    # Sort citations in descending order
    citations.sort(reverse=True)
    h_index = 0
    # Find the largest h such that the author has at least h papers with h citations each
    for i, citation in enumerate(citations, start=1):
        if citation >= i:
            h_index = i
        else:
            break
    return h_index


def main():
    # Read the citation counts from the file
    filename = "u02-hirschindex-example.txt"
    citations = []
    try:
        with open(filename, "r") as file:
            for line in file:
                # Each line is in the format: "DBLP_key\tcitation_count"
                parts = line.strip().split("\t")
                if len(parts) == 2 and parts[1].isdigit():
                    citations.append(int(parts[1]))
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return

    # Calculate the H-index
    h_index = calculate_h_index(citations)

    # Print the result
    print(f"The Hirsch index (H-index) is: {h_index}")


if __name__ == "__main__":
    main()

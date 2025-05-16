class SparseMatrix:
    def __init__(self, file_path=None, num_rows=0, num_cols=0):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.data = []

        if file_path:
            self.load_from_file(file_path)

    def load_from_file(self, file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()

        self.data = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith("rows="):
                self.num_rows = int(line.split('=')[1])
            elif line.startswith("cols="):
                self.num_cols = int(line.split('=')[1])
            else:
                if not (line.startswith("(") and line.endswith(")")):
                    raise ValueError("Input file has wrong format")

                line_content = line[1:-1]
                parts = line_content.split(',')
                if len(parts) != 3:
                    raise ValueError("Input file has wrong format")

                try:
                    row = int(parts[0].strip())
                    col = int(parts[1].strip())
                    value = int(parts[2].strip())
                except:
                    raise ValueError("Input file has wrong format")

                self.data.append([row, col, value])

    def get_element(self, row, col):
        for entry in self.data:
            if entry[0] == row and entry[1] == col:
                return entry[2]
        return 0

    def set_element(self, row, col, value):
        for entry in self.data:
            if entry[0] == row and entry[1] == col:
                entry[2] = value
                return
        self.data.append([row, col, value])

    def add(self, other):
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrix dimensions must match for addition.")

        result = SparseMatrix(num_rows=self.num_rows, num_cols=self.num_cols)

        for row, col, val in self.data:
            result.set_element(row, col, val)

        for row, col, val in other.data:
            current = result.get_element(row, col)
            result.set_element(row, col, current + val)

        return result

    def subtract(self, other):
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrix dimensions must match for subtraction.")

        result = SparseMatrix(num_rows=self.num_rows, num_cols=self.num_cols)

        for row, col, val in self.data:
            result.set_element(row, col, val)

        for row, col, val in other.data:
            current = result.get_element(row, col)
            result.set_element(row, col, current - val)

        return result

    def multiply(self, other):
        if self.num_cols != other.num_rows:
            raise ValueError("Matrix dimensions incompatible for multiplication.")

        result = SparseMatrix(num_rows=self.num_rows, num_cols=other.num_cols)

        for i, j, val1 in self.data:
            for k, l, val2 in other.data:
                if k == j:
                    old_val = result.get_element(i, l)
                    result.set_element(i, l, old_val + val1 * val2)

        return result

    def print_matrix(self):
        print(f"rows={self.num_rows}")
        print(f"cols={self.num_cols}")
        for row, col, val in self.data:
            print(f"({row}, {col}, {val})")


def main():
    print("Welcome to Sparse Matrix Operations!")
    print("Choose the operation:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    
    choice = input("Enter your choice (1/2/3): ")

    file1 = input("Enter the path to the first matrix file: ")
    file2 = input("Enter the path to the second matrix file: ")
    
    try:
        m1 = SparseMatrix(file1)
        m2 = SparseMatrix(file2)

        if choice == '1':
            result = m1.add(m2)
            print("\nResult of Addition:")
            result.print_matrix()

        elif choice == '2':
            result = m1.subtract(m2)
            print("\nResult of Subtraction:")
            result.print_matrix()

        elif choice == '3':
            result = m1.multiply(m2)
            print("\nResult of Multiplication:")
            result.print_matrix()

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
    
    except ValueError as ve:
        print("Error:", ve)


if __name__ == "__main__":
    main()

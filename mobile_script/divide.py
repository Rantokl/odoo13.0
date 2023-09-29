def find_peak(matrix):
    def is_peak(mid_row, col):
        # Check if the element is greater than or equal to its neighbors
        top = matrix[mid_row - 1][col] if mid_row > 0 else float('-inf')
        bottom = matrix[mid_row + 1][col] if mid_row < len(matrix) - 1 else float('-inf')
        left = matrix[mid_row][col - 1] if col > 0 else float('-inf')
        right = matrix[mid_row][col + 1] if col < len(matrix[0]) - 1 else float('-inf')
        
        return matrix[mid_row][col] >= top and matrix[mid_row][col] >= bottom and matrix[mid_row][col] >= left and matrix[mid_row][col] >= right

    def find_peak_in_column(left, right, mid_col):
        mid_row = max(range(left, right + 1), key=lambda row: matrix[row][mid_col])
        if is_peak(mid_row, mid_col):
            return (mid_row, mid_col)
        elif matrix[mid_row][mid_col - 1] > matrix[mid_row][mid_col]:
            return find_peak_in_column(left, mid_col - 1, mid_col - 1)
        else:
            return find_peak_in_column(mid_col + 1, right, mid_col + 1)

    num_rows = len(matrix)
    num_cols = len(matrix[0])
    
    return find_peak_in_column(0, num_cols - 1, num_cols // 2)

# Example usage:
matrix = [
    [20, 22, 21, 25],
    [51, 61, 17, 82],
    [9, 10, 11, 12],
    [4, 3, 2, 1]
]

peak = find_peak(matrix)
print(f"Peak found at position ({peak[0]}, {peak[1]}) with value {matrix[peak[0]][peak[1]]}")

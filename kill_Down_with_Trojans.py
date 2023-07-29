import numpy as np
import scipy
neg_inf = -10000000000
def load_input_file(file_name):
    with open(file_name, 'r') as file:
        n, H = map(int, file.readline().split())
        tile_types = np.zeros((n, n), dtype=int)
        tile_values = np.zeros((n, n), dtype=int)

        for i in range(n * n):
            if i == 0:
                continue  # the initial tile is zero type with zero value
            x, y, t, v = map(int, file.readline().split())
            tile_types[x][y] = t
            tile_values[x][y] = v

    return n, H, tile_types, tile_values


def print_tile_data(tile_types, tile_values):
    print("Tile Types:")
    print(tile_types)
    print("\nTile Values:")
    print(tile_values)


def DP(n, H, tile_types, tile_values):
    # TODO
    # Placeholder function - implement your logic here
    # Your code to check whether it is possible to reach the bottom-right
    # corner without running out of HP should go here.
    # You should use dynamic programming to solve the problem.
    # Return True if possible, False otherwise.

    # By defualt we return False
    # TODO you should change this
    memo = [[None for _ in range(n)] for _ in range(n)]
    res = helper(memo,H, tile_types, tile_values,cur_x=n-1,cur_y=n-1) 
    #print(res)
    attributes_dict = vars(res)
    largest_value = max(attributes_dict.values())
    #print(largest_value)
    is_greater_than_zero = largest_value > 0
    #print(is_greater_than_zero)
    return is_greater_than_zero

class health_counter:
    def __init__(self, value1, value2, value3, value4):
        self.no_token = value1
        self.prot_token = value2
        self.mult_token = value3
        self.both_tokens = value4
    def __str__(self):
        return f"self.no_token: {self.no_token}, self.prot_token: {self.prot_token}, self.mult_token: {self.mult_token}, self.both_tokens: {self.both_tokens}"

def helper(memo,H,tile_types,tile_values,cur_x,cur_y):
    if memo[cur_x][cur_y] != None:
        return memo[cur_x][cur_y]
    elif [cur_x,cur_y] == [0,0]:
        return health_counter(H,neg_inf,neg_inf,neg_inf)
    elif cur_x < 0 or cur_y<0:
        return health_counter(neg_inf,neg_inf,neg_inf,neg_inf)
    elif tile_types[cur_x,cur_y] == 0: #damage done case
        d = tile_values[cur_x,cur_y]
        from_above = helper(memo,H,tile_types,tile_values,cur_x-1,cur_y)
        from_left = helper(memo,H,tile_types,tile_values,cur_x,cur_y-1)
        max_both = max(from_above.both_tokens-d,from_left.both_tokens-d)
        max_mult = max(from_above.mult_token-d,from_left.mult_token-d,from_above.both_tokens,from_left.both_tokens)
        max_prot = max(from_above.prot_token-d,from_left.prot_token-d)
        max_no = max(from_above.no_token-d,from_left.no_token-d,from_above.prot_token,from_left.prot_token)
        memo[cur_x][cur_y] =  health_counter(max_no,max_prot,max_mult,max_both)
    elif tile_types[cur_x,cur_y] == 1: #healing done case
        h = tile_values[cur_x,cur_y]
        from_above = helper(memo,H,tile_types,tile_values,cur_x-1,cur_y)
        from_left = helper(memo,H,tile_types,tile_values,cur_x,cur_y-1)
        max_both = max(from_above.both_tokens+h,from_left.both_tokens+h)
        max_mult = max(from_above.mult_token+h,from_left.mult_token+h)
        max_prot = max(from_above.prot_token+h,from_left.prot_token+h,from_above.both_tokens+(2*h),from_left.both_tokens+(2*h))
        max_no = max(from_above.no_token+h,from_left.no_token+h,from_above.mult_token+(2*h),from_left.mult_token+(2*h))
        memo[cur_x][cur_y] =  health_counter(max_no,max_prot,max_mult,max_both)
    elif tile_types[cur_x,cur_y] == 2: #Protection token added case
        from_above = helper(memo,H,tile_types,tile_values,cur_x-1,cur_y)
        from_left = helper(memo,H,tile_types,tile_values,cur_x,cur_y-1)
        max_both = max(from_above.both_tokens,from_left.both_tokens,from_above.mult_token,from_left.mult_token)
        max_prot = max(from_above.prot_token,from_left.prot_token,from_above.no_token,from_left.no_token)
        memo[cur_x][cur_y] =  health_counter(neg_inf,max_prot,neg_inf,max_both)
    elif tile_types[cur_x,cur_y] == 3: #Multiplication token added case
        from_above = helper(memo,H,tile_types,tile_values,cur_x-1,cur_y)
        from_left = helper(memo,H,tile_types,tile_values,cur_x,cur_y-1)
        max_both = max(from_above.both_tokens,from_left.both_tokens,from_above.prot_token,from_left.prot_token)
        max_mult = max(from_above.mult_token,from_left.mult_token,from_above.no_token,from_left.no_token)
        memo[cur_x][cur_y] =  health_counter(neg_inf,neg_inf,max_mult,max_both)


    #print(f"cur_x:{cur_x},cur_y:{cur_y}, value:{memo[cur_x][cur_y]}")

    return memo[cur_x][cur_y]

def write_output_file(output_file_name, result):
    with open(output_file_name, 'w') as file:
        file.write(str(int(result)))


def main(input_file_name):
    n, H, tile_types, tile_values = load_input_file(input_file_name)
    print_tile_data(tile_types, tile_values)
    result = DP(n, H, tile_types, tile_values)
    print("Result: " + str(result))
    output_file_name = input_file_name.replace(".txt", "_out.txt")
    write_output_file(output_file_name, result)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python kill_Down_with_Trojans.py a_file_name.txt")
    else:
        main(sys.argv[1])

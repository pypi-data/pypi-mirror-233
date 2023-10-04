

def sum_even(start, end):
    sum_of_evens = 0
    for num in range(start, end + 1):
        if num % 2 == 0:
            sum_of_evens += num
    return sum_of_evens


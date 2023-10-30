from itertools import combinations_with_replacement
def list_thresholds():

    list_1 = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    list_2 = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0]
    combination_1= combinations_with_replacement(list_1, 2)
    combination_2 = combinations_with_replacement(list_2, 2)
    combination = list(combination_1) + list(combination_2)
    combination_no_duplicates = list(dict.fromkeys(combination))

    return combination_no_duplicates

print(list_thresholds())
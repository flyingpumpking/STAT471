# lab.py


from pathlib import Path
import io
import pandas as pd
import numpy as np
from dateutil.rrule import rrule


# ---------------------------------------------------------------------
# QUESTION 0
# ---------------------------------------------------------------------


def consecutive_ints(ints):
    """
    :param ints: a list of integers
    :return: True if there exist at least a pair of consecutive integers in the list, otherwise False
    """
    for i in ints:
        if i + 1 in ints or i - 1 in ints:
            return True
    return False

# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def median_vs_mean(nums):
    """
    :param nums: a list of integers
    :return: True if median is less than or equal to the mean, otherwise False
    """
    if len(nums) == 0:
        return False
    sorted_num = sorted(nums)
    mean = sum(sorted_num) / len(sorted_num)
    if len(sorted_num) % 2 == 0:
        return mean >= (sorted_num[len(sorted_num) // 2] + sorted_num[len(sorted_num) // 2 - 1]) / 2
    else:
        return mean >= sorted_num[len(sorted_num) // 2]

# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def same_diff_ints(ints):
    """
    :param ints: a list of integers
    :return: True if there exist two list elements i positions apart, whose absolute difference as integers is also i, otherwise False
    """
    for i in range(len(ints)):
        for j in range(i + 1, len(ints)):
            if abs(ints[i] - ints[j]) == j - i:
                return True
    return False


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def n_prefixes(s, n):
    """
    :param s: a string
    :param n: a positive integer
    :return: a string containing the first `n` consecutive prefixes of `s` in reverse order
    """
    ans = ""
    while n > 0:
        ans += s[:n]
        n -= 1
    return ans


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def exploded_numbers(ints, n):
    """
    :param ints: a list of integers
    :param n: a non-negative integer
    :return: a list of strings containing numbers from the list expanded by `n` numbers in both directions, separated by spaces
    """
    ans = []
    item_len = len(str(max(ints) + n))
    for i in ints:
        tmp = ""
        for j in range(i - n, i + n + 1): # [i - n, i + n]
            j_len = len(str(j))
            if j_len < item_len:
                tmp += str(j).zfill(item_len)
            else:
                tmp += str(j)
            if j < i + n:
                tmp += " "
        ans.append(tmp)
    return ans


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def add_root(A):
    """
    any kinds of loop are forbidden
    :param A: a numpy array
    :return: a new `numpy` array that contains the element-wise sum of the elements in `A` with the square roots of the positions of the elements in `A`
    """
    ans = A + np.sqrt(np.arange(len(A)))
    return ans

def where_square(A):
    """
    :param A: a numpy array
    :return: a new `numpy` array of Booleans whose `i`th element is `True` if and only if the `i`th element of `A` is a perfect square
    """
    return A == np.sqrt(A).astype(int)**2

# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def growth_rates(A):
    """
    any kinds of loop are forbidden
    :param A: a numpy array of stock prices for a single stock on successive days in USD
    :return: an array of growth rates.
    """
    ans = np.diff(A) / A[:-1] # A[:-1] is A[0:len(A) - 1]
    ans = np.round(ans, 2)
    return ans

def with_leftover(A):
    """
    np.cumsum is useful, any kinds of loop are forbidden
    :param A: a numpy array of stock prices
    :return: the day (as an `int`) on which you can buy at least one full share using just "left-over" money
    """
    leftover = np.cumsum(20 % A)
    days = np.where(leftover - A >= 0)[0]
    return int(days[0]) if days.size > 0 else -1


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def salary_stats(salary):
    """
    :param salary: a DataFrame
    :return: a Series containing:
    num_players: the number of players,
    num_teams: the number of teams,
    total_salary: the total salary amount for all players,
    highest_salary: the name of the player with the highest salary,
    avg_los: the average salary of the Los Angeles Lakers, rounded to two decimal places,
    fifth_lowest: the name and team of the player who has the fifth-lowest salary, separated by a comma and a space e.g. "Kobe Bryant, Los Angeles Lakers",
    duplicates: a boolean that is true if there are ny duplicate las names, and false otherwise,
    Note that some players may have a suffix on their name, such as "Jr." or "III" -- you should ignore these.
    For example, "Billy Triton Jr." and "Tyler Triton" should be considered to have the same last name.
    total_highest: the total salary of the team that has the highest paid player
    """
    last_names = salary['Player'].str.extract(r'(\w+)(?:\s+(?:Jr\.|II|III))?$')[0]
    fifth_lowest_array = salary.sort_values("Salary").iloc[4][["Player", "Team"]].values.tolist()
    fifth_lowest = ", ".join(fifth_lowest_array)
    data = [
        ["num_players", len(salary)],
        ["num_teams", len(salary["Team"].unique())],
        ["total_salary", salary["Salary"].sum()],
        ["highest_salary", salary["Player"].max()],
        ["avg_los", round(salary[salary["Team"] == "Los Angeles Lakers"]["Salary"].mean(), 2)],
        ["fifth_lowest", fifth_lowest],
        ["duplicates", last_names.duplicated().any()],
        ["total_highest", salary[salary["Team"] == salary["Team"].max()]["Salary"].sum()]
    ]
    # use the first column as the index
    return pd.Series(dict(data), name="Salary Stats")

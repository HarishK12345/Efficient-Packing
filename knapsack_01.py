def knapsack_dynamic_programming(names,weights, values, capacity):
    n = len(weights)
    # Create a table to store the maximum values for different weights and items
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            # If the current item's weight is less than or equal to the current capacity
            if weights[i - 1] <= w:
                # Take the maximum value between including the current item and excluding the current item
                dp[i][w] = max(values[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w])
            else:
                # If the current item's weight is greater than the current capacity, exclude it
                dp[i][w] = dp[i - 1][w]

    # Find the items included in the knapsack by backtracking through the table
    included = []
    i, w = n, capacity
    while i > 0 and w > 0:
        if dp[i][w] != dp[i - 1][w]:
            included.append(i - 1)
            w -= weights[i - 1]
        i -= 1

    # Reverse the list of included items to match the original order
    included.reverse()
    included_itemlist=[names[i] for i in included]
    # included_items="\n"
    # for i in included_itemlist:
    #     included_items+=i+", "
    notincluded=[]
    for i in names:
        if i not in included_itemlist:
            notincluded.append(i)
    return (dp[n][capacity],included_itemlist,capacity),notincluded

if __name__=="__main__":
    # Example usage:
    names = ['a','b','c','d']
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 5

    max_value, notinc = knapsack_dynamic_programming(names,weights, values, capacity)
    print("Max Value:", max_value)
    print("NotIncluded Items:", notinc)

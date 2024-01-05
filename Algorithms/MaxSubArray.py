
'''
Ryan Moore
CS 5800: Introduction to Algorithms

This Python code is an implementation of a solution to find the maximum product subarray in an array of integers. 
The solution is based on a divide-and-conquer approach. Let's break down the key components of the code:
'''
class Solution:

    def max_crossing(self, nums, low, mid, high):
        '''
        - This method calculates the maximum product of a subarray that crosses the midpoint of the array.
        - It considers both positive and negative products separately for the left and right subarrays 
            and calculates the maximum product that can be obtained by combining both halves.
        - The final result, `max_prod`, is the maximum of four possibilities: 
            `max_pos_r`, `max_pos_l`, `max_pos_r * max_pos_l`, and `max_neg_r * max_neg_l`.
        '''
        max_pos_l, max_neg_l, prod = -1, 1, 1

        # calculate pos/neg products of left sub array
        for i in range(mid, low - 1, -1):
            prod *= nums[i]
            max_pos_l = max(max_pos_l, prod)
            max_neg_l = min(max_neg_l, prod)

        max_pos_r, max_neg_r, prod = -1, 1, 1

        # calculate pos/neg products of right subarray
        for i in range(mid + 1, high + 1):
            prod *= nums[i]
            max_pos_r = max(max_pos_r, prod)
            max_neg_r = min(max_neg_r, prod)

        # calculate the maximum positive product crossing the midpoint
        max_prod = max(max_pos_r, max_pos_l, max_pos_r * max_pos_l, max_neg_r * max_neg_l)

        return max_prod

    def max_sub_array(self, nums, low, high):
        '''
        - This method is a recursive function that uses a divide-and-conquer approach to find the maximum product subarray.
        - It calculates the maximum product subarray for the left and right halves of the array, 
            as well as the maximum product subarray that crosses the midpoint, using the `max_crossing` method.
        - The result is the maximum of the three calculated values.
        '''
        if low == high:
            return nums[low]

        mid = (low + high) // 2

        # Compute max product subarray left of mid point
        max_left = self.max_sub_array(nums, low, mid)
        # Compute max product subarray right of mid point
        max_right = self.max_sub_array(nums, mid + 1, high)
        # Compute max product subarray crossing mid point
        max_cross = self.max_crossing(nums, low, mid, high)

        # Return max of all products
        return max(max_left, max_right, max_cross)

    def max_product(self, nums):
        '''
        - This is the main entry point of the solution. 
            It initializes the length of the input array and calls the `max_sub_array` method with the entire array.
        '''
        n = len(nums)
        return self.max_sub_array(nums, 0, n - 1)


# Example usage:
nums = [2, 3, -2, 4]
sol = Solution()
result = sol.max_product(nums)
print(result)

'''
In summary, this code provides a solution to find the maximum product subarray in an array using a divide-and-conquer approach. 
It calculates the maximum product for the left subarray, right subarray, and the subarray crossing the midpoint, 
then returns the maximum of these three values.
'''
class SegmentTree:
    @staticmethod
    def func(left, right):
        return (min(left[0], right[0]),max(left[1], right[1]),max(left[2], right[2], right[1] - left[0]))
    def __init__(self, arr):
        arr = [0] + arr
        for i in range(1, len(arr)):
            arr[i] += arr[i - 1]
        self.n1 = len(arr) - 1
        self.n = (1 << ((len(arr) - 1).bit_length()))
        self.tree = [(float('inf'), -float('inf'), -float('inf'))] * (2 * self.n)
        for i in range(len(arr)):
            self.tree[self.n + i] = (arr[i], arr[i], 0)
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.func(self.tree[2 * i], self.tree[2 * i + 1])
    def query(self, l, r):
        """Query range [l, r] inclusive."""
        l += self.n
        r += self.n
        res_left = (float('inf'), -float('inf'), -float('inf'))
        res_right = (float('inf'), -float('inf'), -float('inf'))
        while l <= r:
            if l % 2 == 1:
                res_left = self.func(res_left, self.tree[l])
                l += 1
            if r % 2 == 0:
                res_right = self.func(self.tree[r], res_right)
                r -= 1
            l //= 2
            r //= 2
        return self.func(res_left, res_right)
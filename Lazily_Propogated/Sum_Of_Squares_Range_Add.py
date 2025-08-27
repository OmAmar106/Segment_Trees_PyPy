class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.sum = [0] * (4 * self.n)  
        self.sumSquares = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)   
        self.build(arr, 1, 0, self.n - 1)
    def build(self, arr, node, l, r):
        if l == r:
            self.sum[node] = arr[l]
            self.sumSquares[node] = arr[l] * arr[l]
        else:
            mid = (l + r) // 2
            self.build(arr, node*2, l, mid)
            self.build(arr, node*2+1, mid+1, r)
            self.push_up(node)
    def push_up(self, node):
        self.sum[node] = self.sum[node*2] + self.sum[node*2+1]
        self.sumSquares[node] = self.sumSquares[node*2] + self.sumSquares[node*2+1]
    def apply(self, node, l, r, val):
        length = r-l+1
        self.sumSquares[node] += 2 * val * self.sum[node] + length * val * val
        self.sum[node] += length * val
        self.lazy[node] += val
    def push_down(self, node, l, r):
        if self.lazy[node] != 0:
            mid = (l + r) // 2
            self.apply(node*2, l, mid, self.lazy[node])
            self.apply(node*2+1, mid+1, r, self.lazy[node])
            self.lazy[node] = 0
    def update(self, ql, qr, val, node=1, l=0, r=None):
        # add val from ql to qr inclusive
        if r is None:
            r = self.n - 1
        if ql > r or qr < l:
            return
        if ql <= l and r <= qr:
            self.apply(node, l, r, val)
            return
        self.push_down(node, l, r)
        mid = (l + r) // 2
        self.update(ql, qr, val, node*2, l, mid)
        self.update(ql, qr, val, node*2+1, mid+1, r)
        self.push_up(node)
    def query(self, ql, qr, node=1, l=0, r=None):
        # query from ql to qr
        if r is None:
            r = self.n - 1
        if ql > r or qr < l:
            return 0
        if ql <= l and r <= qr:
            return self.sumSquares[node]
        self.push_down(node, l, r)
        mid = (l + r) // 2
        return self.query(ql, qr, node*2, l, mid) + self.query(ql, qr, node*2+1, mid+1, r)

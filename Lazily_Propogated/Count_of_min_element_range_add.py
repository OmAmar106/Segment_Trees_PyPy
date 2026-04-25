
class Node:
    def __init__(self,val,count=1):
        self.val = val
        self.count = count
    def func(left,right):
        if right is None:
            if left is None:
                return None
            return left
        elif left is None:
            return right
        if left.val<right.val:return Node(left.val,left.count)
        elif left.val>right.val:return Node(right.val,right.count)
        else:return Node(left.val,left.count+right.count)
    def add(self,val):
        self.val += val
class SegmentTree:
    class _RangeProxy:
        def __init__(self, seg, sl):
            self.seg, self.sl = seg, sl
        def __iadd__(self, v):
            self.seg.range_update(self.sl.start, self.sl.stop-1, v, True)
            return self
        def __repr__(self):
            return str(self.seg.range_query(self.sl.start, self.sl.stop-1))
    def __getitem__(self, k):
        if isinstance(k, slice):
            return SegmentTree._RangeProxy(self, k)
        return self.range_query(k, k)
    def __setitem__(self, k, v):
        if isinstance(v, SegmentTree._RangeProxy):
            return
        if isinstance(k, slice):
            self.range_update(k.start, k.stop-1, v, False)
        else:
            self.range_update(k, k, v, False)
    def __init__(self, data,func=Node.func):
        self.func = func
        self.n = len(data)
        self.size = 1 << (self.n - 1).bit_length()
        self.tree = [None for i in range (2 * self.size)]
        self._size = [0] * (2 * self.size)
        self._size[self.size:] = [1] * self.size
        for i in range(self.size - 1, 0, -1):
            self._size[i] = self._size[i << 1] + self._size[i << 1 | 1]
        self.lazy_add = 0
        self.lazy_add = [0] * self.size
        for i in range(self.n):
            self.tree[self.size + i] = Node(data[i])
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = self.func(self.tree[i << 1], self.tree[i << 1 | 1])
    def _apply_set(self, pos, value):
        self.tree[pos].set(value)
        if pos < self.size:
            self.lazy_add[pos] = 0
    def _apply_add(self, pos, value):
        self.tree[pos].add(value)
        if pos < self.size:
            self.lazy_add[pos] += value
    def _build(self, pos):
        while pos > 1:
            pos >>= 1
            self.tree[pos] = self.func(self.tree[pos << 1], self.tree[pos << 1 | 1])
            if self.lazy_add[pos] != 0:
                self.tree[pos].add(self.lazy_add[pos])
    def _push(self, pos):
        for shift in range(self.size.bit_length() - 1, 0, -1):
            i = pos >> shift
            add_val = self.lazy_add[i]
            if add_val != 0:
                self._apply_add(i << 1, add_val)
                self._apply_add(i << 1 | 1, add_val)
                self.lazy_add[i] = 0
    def range_update(self, left, right, value,flag=True):
        # Range Update in [L,R] if flag, then add
        l = left + self.size
        r = right + self.size
        l0, r0 = l, r
        self._push(l0)
        self._push(r0)
        while l <= r:
            if l & 1: self._apply_add(l, value); l += 1
            if not r & 1: self._apply_add(r, value); r -= 1
            l >>= 1; r >>= 1
        self._build(l0)
        self._build(r0)
    def range_query(self, left, right):
        # Range Query in [L,R]
        l = left + self.size
        r = right + self.size
        self._push(l)
        self._push(r)
        lefty = None
        righty = None
        while l <= r:
            if l & 1: lefty = Node.func(lefty,self.tree[l]); l += 1
            if not r & 1: righty = Node.func(self.tree[r],righty); r -= 1
            l >>= 1; r >>= 1
        return Node.func(lefty,righty)

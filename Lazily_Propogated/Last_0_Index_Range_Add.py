# https://leetcode.com/problems/longest-balanced-subarray-ii/submissions/1808940387

def f(a,b):
    return (min(a[0],b[0]),max(a[1],b[1]))
def f2(x):
    return x[0]<=0<=x[1]
class SegmentTree:
    def __init__(self,arr):
        self.n = (1<<(len(arr)-1).bit_length())
        self.n1 = len(arr)
        self.tree = [(float('inf'),-float('inf'))]*(2*self.n)
        self.lazy = [0]*(2*self.n)
        self.build(arr,1,0,self.n1-1)
    def build(self,arr,node,start,end):
        if start==end:
            self.tree[node] = (arr[start],arr[start])
            return
        mid = (start+end)//2
        self.build(arr,2*node,start,mid)
        self.build(arr,2*node+1,mid+1,end)
        self.tree[node] = f(self.tree[2*node],self.tree[2*node+1])
    def push(self,node,l,r):
        if self.lazy[node]:
            self.tree[node] = (self.tree[node][0]+self.lazy[node],self.tree[node][1]+self.lazy[node])
            if l!=r:
                self.lazy[2*node] += self.lazy[node]
                self.lazy[2*node+1] += self.lazy[node]
            self.lazy[node] = 0
    def update(self,node,l,r,start,end,val):
        self.push(node,l,r)
        if start<=l and r<=end:
            self.lazy[node] += val
            self.push(node,l,r)
            return
        if start>r or end<l:return
        mid = (l+r)//2
        self.update(2*node,l,mid,start,end,val)
        self.update(2*node+1,mid+1,r,start,end,val)
        self.tree[node] = f(self.tree[2*node],self.tree[2*node+1])
    def range_add(self,start,end,val):
        self.update(1,0,self.n1-1,start,end,val)
    def query(self,node,start,end,r):
        self.push(node,start,end)
        if end<r:
            return -float('inf')
        if start==end:
            return end
        mid = (start+end)//2
        self.push(2*node+1,mid+1,end)
        self.push(2*node,start,mid)
        if f2(self.tree[2*node+1]):
            return self.query(2*node+1,mid+1,end,r)
        else:
            return self.query(2*node,start,mid,r)
    def last(self,r):
        return self.query(1,0,self.n1-1,r)
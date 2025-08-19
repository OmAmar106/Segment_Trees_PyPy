class SegmentTree:
    def __init__(self,n):
        self.n1 = n
        self.n = (1<<((n-1).bit_length()+1))
        self.tree = [0]*(2*self.n)
        self.lazy = [0]*(2*self.n)
    def push(self,node,l,r):
        if self.lazy[node]:
            self.tree[node] += self.lazy[node]*(r-l+1)
            if l!=r:
                self.lazy[2*node] += self.lazy[node]
                self.lazy[2*node+1] += self.lazy[node]
            self.lazy[node] = 0
    def update_(self,start,end,node,l,r,val):
        self.push(node,start,end)
        if r<start or l>end:return
        if r>=end and l<=start:
            self.lazy[node] += val
            self.push(node,start,end)
            return
        mid = (start+end)//2
        self.update_(start,mid,2*node,l,r,val)
        self.update_(mid+1,end,2*node+1,l,r,val)
        self.tree[node] = max(self.tree[2*node],self.tree[2*node+1])
    def update(self,start,end,val):
        self.update_(0,self.n1-1,1,start,end,val)
    def query(self,l):
        start = 0;end = self.n1-1;node = 1
        while start!=end:
            self.push(node,start,end)
            node *= 2;mid = (start+end)//2
            if l<=mid:
                end = mid
            else:
                node += 1
                start = mid+1
        self.push(node,start,end)
        return self.tree[node]
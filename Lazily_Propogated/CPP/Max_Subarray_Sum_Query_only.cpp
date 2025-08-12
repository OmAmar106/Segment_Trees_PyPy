
class SegmentTree{
    vector<tuple<int,int,int>> tree;
    int n;
    int n1;
    public:

        tuple<int,int,int> func(tuple<int,int,int> &a,tuple<int,int,int> &b){
            tuple<int,int,int> tpnew;
            tpnew = {min(get<0>(a),get<0>(b)),max(get<1>(a),get<1>(b)),max(max(get<2>(a),get<2>(b)),get<1>(b)-get<0>(a))};
            return tpnew;
        }

        SegmentTree(vi L){
            n = len(L);
            n1 = 1;
            while (n1 < n) n1 <<= 1;
            tree.assign(2*n1, {INF, -INF, -INF});
            
            for(int i=0;i<len(L);i++){
                tree[i+n1] = {L[i],L[i],0};
            }

            for(int i=n1-1;i>0;i--){
                tree[i] = func(tree[2*i],tree[2*i+1]);
            }
        }

        tuple<int,int,int> query(int l,int r){
            l += n1;
            r += n1;
            tuple<int,int,int> left = {INF,-INF,-INF};
            tuple<int,int,int> right = {INF,-INF,-INF};
            while(l<=r){
                if(l&1){
                    left = func(left,tree[l]);
                    l++;
                }
                if(!(r&1)){
                    right = func(tree[r],right);
                    r--;
                }
                l >>= 1;
                r >>= 1;
            }
            return func(left,right);
        }
};

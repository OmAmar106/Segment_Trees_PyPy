#include <bits/stdc++.h>
using namespace std;

struct LiChao {
    struct Node {
        int lo, hi, mid;
        long long m, b;
        bool has_line;
        Node *left, *right;
        Node(int l, int r)
            : lo(l), hi(r), mid((l + r) >> 1),
              m(0), b(0), has_line(false),
              left(nullptr), right(nullptr) {}
    };
    Node* root;
    LiChao(int l, int r) {
        root = new Node(l, r);
    }
    void add_line(long long m, long long b) {
        Node* node = root;
        while (true) {
            int lo = node->lo, hi = node->hi, mid = node->mid;
            if (!node->has_line) {
                node->m = m;
                node->b = b;
                node->has_line = true;
                return;
            }
            long long cur_m = node->m, cur_b = node->b;
            if (m * mid + b > cur_m * mid + cur_b) {
                swap(node->m, m);
                swap(node->b, b);
                cur_m = node->m;
                cur_b = node->b;
            }
            if (lo == hi) return;
            if (m * lo + b > cur_m * lo + cur_b) {
                if (!node->left)
                    node->left = new Node(lo, mid);
                node = node->left;
            }
            else if (m * hi + b > cur_m * hi + cur_b) {
                if (!node->right)
                    node->right = new Node(mid + 1, hi);
                node = node->right;
            }
            else return;
        }
    }

    long long query(int x) {
        Node* node = root;
        long long res = LLONG_MIN;
        while (node) {
            if (node->has_line) {
                res = max(res, node->m * x + node->b);
            }
            if (node->lo == node->hi) break;
            if (x <= node->mid) node = node->left;
            else node = node->right;
        }
        return res;
    }
};

struct SegmentTree {
    int n;
    vector<LiChao*> tree;
    SegmentTree(int n) : n(n) {
        tree.resize(4 * n);
        for (int i = 0; i < 4 * n; i++) {
            tree[i] = new LiChao(0, n);
        }
    }
    void update(int idx, int l, int r, int ql, int qr, long long m, long long c) {
        stack<tuple<int,int,int>> st;
        st.push({idx, l, r});
        while (!st.empty()) {
            auto [i, L, R] = st.top(); st.pop();
            if (R < ql || L > qr) continue;
            if (ql <= L && R <= qr) {
                tree[i]->add_line(m, c);
                continue;
            }
            int mid = (L + R) >> 1;
            st.push({2*i+1, mid+1, R});
            st.push({2*i, L, mid});
        }
    }
    long long query(int idx, int l, int r, int pos) {
        long long ans = LLONG_MIN;
        while (l < r) {
            int mid = (l + r) >> 1;
            ans = max(ans, tree[idx]->query(pos));
            if (pos > mid) {
                l = mid + 1;
                idx = 2*idx + 1;
            } else {
                r = mid;
                idx = 2*idx;
            }
        }
        ans = max(ans, tree[idx]->query(pos));
        return ans;
    }
};

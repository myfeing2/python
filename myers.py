def diff(a, b):
   n, m = len(a), len(b)
   max_d = n + m
   v = {1: 0}
   trace = []
   for d in range(max_d + 1):
       trace.append(v.copy())
       
       for k in range(-d, d + 1, 2):
           print(v, k, -d, d+1)
           if k == -d or (k != d and v[k - 1] < v[k + 1]):
               x = v[k + 1]
           else:
               x = v[k - 1] + 1
           y = x - k
           while x < n and y < m and a[x] == b[y]:
               x, y = x + 1, y + 1
           v[k] = x
           if x >= n and y >= m:
               return reconstruct(trace, a, b)
   return []

def reconstruct(trace, a, b):
   # Backtracking to produce edit script (simplified)
   edits = []
   x, y = len(a), len(b)
   for d in reversed(range(len(trace))):
       v = trace[d]
       k = x - y
       if k == -d or (k != d and v[k - 1] < v[k + 1]):
           prev_k = k + 1
       else:
           prev_k = k - 1
       prev_x = v[prev_k]
       prev_y = prev_x - prev_k
       while x > prev_x and y > prev_y:
           edits.append(("MATCH", a[x - 1]))
           x, y = x - 1, y - 1
       if x == prev_x:
           edits.append(("INSERT", b[y - 1]))
           y -= 1
       else:
           edits.append(("DELETE", a[x - 1]))
           x -= 1
   return edits[::-1]


print(diff("ABCABBA", "CBABAC"))
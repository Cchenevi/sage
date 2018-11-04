## -*- encoding: utf-8 -*-
"""
This file (./sol/numbertheory_doctest.sage) was *autogenerated* from ./sol/numbertheory.tex,
with sagetex.sty version 2011/05/27 v2.3.1.
It contains the contents of all the sageexample environments from this file.
You should be able to doctest this file with:
sage -t ./sol/numbertheory_doctest.sage
It is always safe to delete this file; it is not used in typesetting your
document.

Sage example in ./sol/numbertheory.tex, line 9::

  sage: def enum_carmichael(N, verbose=True):
  ....:    p = 3; s = 0
  ....:    while p^3 <= N:
  ....:       s += enum_carmichael_p(N, p, verbose); p = next_prime(p)
  ....:    return s

Sage example in ./sol/numbertheory.tex, line 26::

  sage: def enum_carmichael_p (n, p, verbose):
  ....:    a = p; m = p*(p-1); q = p; s = 0
  ....:    while p*q^2 <= n:
  ....:       q = next_prime(q)
  ....:       s += enum_carmichael_pq(n, a, m, p, q, verbose)
  ....:    return s

Sage example in ./sol/numbertheory.tex, line 52::

  sage: def enum_carmichael_pq(n,a,m,p,q,verbose):
  ....:    if (a-q) % gcd(m,q*(q-1)) != 0: return 0
  ....:    s = 0
  ....:    a = crt (a, q, m, q*(q-1)); m = lcm(m,q*(q-1))
  ....:    while a <= p*q^2: a += m
  ....:    for t in range(a, n+1, m):
  ....:       r = t // (p*q)
  ....:       if is_prime(r) and t % (r-1) == 1:
  ....:          if verbose:
  ....:             print((p*q*r, factor(p*q*r)))
  ....:          s += 1
  ....:    return s

Sage example in ./sol/numbertheory.tex, line 68::

  sage: enum_carmichael(10^4)
  (561, 3 * 11 * 17)
  (1105, 5 * 13 * 17)
  (2465, 5 * 17 * 29)
  (1729, 7 * 13 * 19)
  (2821, 7 * 13 * 31)
  (8911, 7 * 19 * 67)
  (6601, 7 * 23 * 41)
  7
  sage: enum_carmichael(10^5, False)
  12
  sage: enum_carmichael(10^6, False)
  23
  sage: enum_carmichael(10^7, False)
  47

Sage example in ./sol/numbertheory.tex, line 94::

  sage: def aliq(n):
  ....:    l = [n]
  ....:    while n != 1:
  ....:       n = sigma(n) - n
  ....:       if n in l: break
  ....:       l.append(n)
  ....:    return l
  sage: l = aliq(840)
  sage: len(l), l[:5], l[-5:]
  (748, [840, 2040, 4440, 9240, 25320], [2714, 1606, 1058, 601, 1])

Sage example in ./sol/numbertheory.tex, line 106::

  sage: p = points([(i, log(l[i])/log(10)) for i in range(len(l))])

Sage example in ./sol/numbertheory.tex, line 173::

  sage: def rk_aux(xc, yc, d, r2):
  ....:     s = 0
  ....:     xmin = ceil((xc - sqrt(r2))/d)
  ....:     xmax = floor((xc + sqrt(r2))/d)
  ....:     for x in range(xmin,xmax+1):
  ....:         r3 = r2 - (d*x-xc)^2 # (d*y-yc)^2 <= r2 - (d*x-xc)^2
  ....:         ymin = ceil((yc - sqrt(r3))/d)
  ....:         ymax = floor((yc + sqrt(r3))/d)
  ....:         s += ymax + 1 - ymin
  ....:     return s

Sage example in ./sol/numbertheory.tex, line 219::

  sage: def rk(k): # returns (r_k^2, xc, yc)
  ....:     if k == 2: return 1/4, 1/2, 0
  ....:     dmax = (2*sqrt(k/pi)).n(); xamax = (sqrt(2*k/pi)).n()
  ....:     sol = (dmax/2)^2, 0, 0, 0
  ....:     for xa in range(0, floor(xamax)+1):
  ....:         # if xa=0, ya > 0 since A should differ from O
  ....:         yamin = max(xa, 1)
  ....:         for ya in range(yamin, floor(sqrt(dmax^2-xa^2))+1):
  ....:             xbmin = 0 # we want xb*ya <= xa^2+ya^2
  ....:             if xa == 0:
  ....:                 xbmin = 1 # O, A, B should not be aligned
  ....:             xbmax = min(floor(dmax), floor((xa*xa+ya*ya)/ya))
  ....:             for xb in range(xbmin, xbmax+1):
  ....:                 ybmax = floor(sqrt(dmax^2-xb^2))
  ....:                 if xa > 0: # we want xb*ya+yb*xa <= xa^2+ya^2
  ....:                     tmp = floor((xa*xa+ya*ya-xb*ya)/xa)
  ....:                     ybmax = min(ybmax, tmp)
  ....:                 # if xb=0, yb > 0 since B should differ from O
  ....:                 ybmin = 0
  ....:                 if xb == 0:
  ....:                     ybmin = 1
  ....:                 for yb in range(ybmin,ybmax+1):
  ....:                     d = 2*abs(xb*ya - xa*yb)
  ....:                     if d != 0:
  ....:                         ra2 = xa^2+ya^2; rb2 = xb^2+yb^2
  ....:                         xc = abs(ra2*yb - rb2*ya)
  ....:                         yc = abs(rb2*xa - ra2*xb)
  ....:                         r2 = ra2*rb2*((xa-xb)^2+(ya-yb)^2)
  ....:                         m = rk_aux(xc,yc,d,r2)
  ....:                         if m >= k and r2/d^2 < sol[0]:
  ....:                             sol = r2/d^2, xc/d, yc/d
  ....:     return sol

Sage example in ./sol/numbertheory.tex, line 253::

  sage: for k in range(2,10): print((k, rk(k)))
  (2, (1/4, 1/2, 0))
  (3, (1/2, 1/2, 1/2))
  (4, (1/2, 1/2, 1/2))
  (5, (1, 0, 1))
  (6, (5/4, 1/2, 1))
  (7, (25/16, 3/4, 1))
  (8, (2, 1, 1))
  (9, (2, 1, 1))

Sage example in ./sol/numbertheory.tex, line 283::

  sage: def plotrk(k):
  ....:    r2, x0, y0 = rk(k); r = n(sqrt(r2))
  ....:    var('x, y')
  ....:    c = implicit_plot((x-x0)^2+(y-y0)^2-r2,
  ....:        (x, x0-r-1/2, x0+r+1/2),(y, y0-r-1/2, y0+r+1/2))
  ....:    center = points([(x0,y0)], pointsize=50, color='black')
  ....:    # we want (i-x0)^2+(j-y0)^2 <= r2
  ....:    # thus |i-x0| <= r and |j-y0| <= r2 - (i-x0)^2
  ....:    l = [(i, j) for i in range(ceil(x0-r), floor(x0+r)+1)
  ....:                for j in range(ceil(y0-sqrt(r^2-(i-x0)^2)),
  ....:                               floor(y0+sqrt(r2-(i-x0)^2))+1)]
  ....:    d = points(l, pointsize=100)
  ....:    return (c+center+d).show(aspect_ratio=1, axes=True)

Sage example in ./sol/numbertheory.tex, line 377::

  sage: x1, x2, s2 = var('x1, x2, s2')
  sage: n1 = 9; C1 = integrate(x1^n1, x1, x2, s2); C1
  1/10*s2^10 - 1/10*x2^10

Sage example in ./sol/numbertheory.tex, line 390::

  sage: x3, s3 = var('x3, s3')
  sage: n2 = 7; C2 = integrate(C1.subs(s2=s3-x2)*x2^n2, x2, x3, s3/2); C2
  44923/229417943040*s3^18 - 1/80*s3^10*x3^8 + 1/9*s3^9*x3^9 - 9/20*s3^8*x3^10
  + 12/11*s3^7*x3^11 - 7/4*s3^6*x3^12 + 126/65*s3^5*x3^13 - 3/2*s3^4*x3^14
  + 4/5*s3^3*x3^15 - 9/32*s3^2*x3^16 + 1/17*s3*x3^17

"""


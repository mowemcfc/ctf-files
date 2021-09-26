from sage.all import *
# Original: https://github.com/mimoo/RSA-and-LLL-attacks/blob/master/boneh_durfee.sage

dimension_min = 7

def remove_unhelpful(BB, monomials, bound, current):
  if current == -1 or BB.dimensions()[0] <= dimension_min:
    return BB
  for ii in range(current, -1, -1):
    if BB[ii, ii] >= bound:
      affected_vectors = 0
      affected_vector_index = 0
      for jj in range(ii + 1, BB.dimensions()[0]):
        if BB[jj, ii] != 0:
          affected_vectors += 1
          affected_vector_index = jj
      if affected_vectors == 0:
        #print "* removing unhelpful vector", ii
        BB = BB.delete_columns([ii])
        BB = BB.delete_rows([ii])
        monomials.pop(ii)
        BB = remove_unhelpful(BB, monomials, bound, ii-1)
        return BB
      elif affected_vectors == 1:
        affected_deeper = True
        for kk in range(affected_vector_index + 1, BB.dimensions()[0]):
          if BB[kk, affected_vector_index] != 0:
            affected_deeper = False
        if affected_deeper and abs(bound - BB[affected_vector_index, affected_vector_index]) < abs(bound - BB[ii, ii]):
          #print "* removing unhelpful vectors", ii, "and", affected_vector_index
          BB = BB.delete_columns([affected_vector_index, ii])
          BB = BB.delete_rows([affected_vector_index, ii])
          monomials.pop(affected_vector_index)
          monomials.pop(ii)
          BB = remove_unhelpful(BB, monomials, bound, ii-1)
          return BB
  return BB

def boneh_durfee_small_roots(pol, modulus, mm, tt, XX, YY):
    PR.<u, x, y> = PolynomialRing(ZZ)
    Q = PR.quotient(x*y + 1 - u) # u = xy + 1
    polZ = Q(pol).lift()
    UU = XX*YY + 1
    gg = []
    for kk in range(mm + 1):
      for ii in range(mm - kk + 1):
        xshift = x^ii * modulus^(mm - kk) * polZ(u, x, y)^kk
        gg.append(xshift)
    gg.sort()
    monomials = []
    for polynomial in gg:
      for monomial in polynomial.monomials():
        if monomial not in monomials:
          monomials.append(monomial)
    monomials.sort()
    for jj in range(1, tt + 1):
      for kk in range(floor(mm/tt) * jj, mm + 1):
        yshift = y^jj * polZ(u, x, y)^kk * modulus^(mm - kk)
        yshift = Q(yshift).lift()
        gg.append(yshift)
        monomials.append(u^kk * y^jj)
    nn = len(monomials)
    BB = Matrix(ZZ, nn)
    for ii in range(nn):
      BB[ii, 0] = gg[ii](0, 0, 0)
      for jj in range(1, ii + 1):
        if monomials[jj] in gg[ii].monomials():
          BB[ii, jj] = gg[ii].monomial_coefficient(monomials[jj]) * monomials[jj](UU,XX,YY)
    BB = remove_unhelpful(BB, monomials, modulus^mm, nn-1)
    nn = BB.dimensions()[0]
    if nn == 0:
      print("failure")
      return 0,0
    BB = BB.LLL()
    PR.<w,z> = PolynomialRing(ZZ)
    pol1 = pol2 = 0
    for jj in range(nn):
      pol1 += monomials[jj](w*z+1,w,z) * BB[0, jj] / monomials[jj](UU,XX,YY)
      pol2 += monomials[jj](w*z+1,w,z) * BB[1, jj] / monomials[jj](UU,XX,YY)
    PR.<q> = PolynomialRing(ZZ)
    rr = pol1.resultant(pol2)
    if rr.is_zero() or rr.monomials() == [1]:
      print("the two first vectors are not independant")
      return 0, 0
    rr = rr(q, q)
    soly = rr.roots()
    if len(soly) == 0:
      print("Your prediction (delta) is too small")
      return 0, 0
    soly = soly[0][0]
    ss = pol1(q, soly)
    solx = ss.roots()[0][0]
    return solx, soly

def boneh_durfee(n, e):
  delta = RR(0.167) # d ~ n^0.167
  m = 5
  t = round((1-2*delta) * m)
  X = ZZ(2*floor(n^delta))
  # we have n = p^2q. so `phi(n) = n + {-(pq+pr+qr) + p+q+r)} - 1`.
  # we reconsidered boneh-durfee's attack then we have `x(A+y) + 1 = 0 mod e` where `A = (n-1)`
  # and (x, y) = (k, -(pq+pr+qr)+p+q+r). 
  Y = ZZ(floor(n^(2/3)))
  P.<x,y> = PolynomialRing(ZZ)
  A = ZZ((n-1)/2)
  pol = 1 + x * (A + y)
  solx, soly = boneh_durfee_small_roots(pol, e, m, t, X, Y)
  print(solx, soly)
  if solx > 0:
    return int(pol(solx, soly) / e)
  return 0

if __name__ == "__main__":
  N = 549935778300831378406948873536278349781214706503360745280597408861216877781142622004454148443526758471040653633080987617044763942008023466559253761306561736450658314626615456982873023501736081710037081947666247132668118860186965548713647775109193997705890766881191577188287773692953347103686449329398217311195051172403636510262250822460785125486925931569891688688353900466632582649417645956790937903144901696446727579207702041958066277574559994377445136251040659
  e = 32204951698260962458157592984992469529416584332675382497988021285424821386904232277036373403101864193040613563796784569698857185940927175841205145358641690922026788366581684507467056308764343250379771013177468030580725648480591696059317745554974780583562695962973324819593002957827750301174079447431501960032717699255546396631743680242345092881301693065171460311485778344053788138555054294470951574964376432654831106364396876336137419860163278539415409181597819
  print(boneh_durfee(N, e))

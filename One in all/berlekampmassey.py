# @author      Michael Foukarakis
# @version     0.1
#------------------------------------------------------------------------
# Description: A class representing polynomials over GF(2).
#              The coefficients are stored in a list.
#              And the Berlekamp-Massey algorithm implementation.
#------------------------------------------------------------------------
from operator import xor
from functools import reduce

class Polynomial(list):
    def __str__(self):
        L = ['{}*x^{}'.format(e, i) for i,e in enumerate(self)]
        return ' + '.join(L)

    def __add__(self, other):
        if len(self) < len(other):
              return other + self
        else:
            k = len(self) - len(other)
            new = [a^b for (a,b) in zip(self,([0]*k)+other)]
            try:
                while new[0] == 0:
                    new.pop(0)
            except IndexError:
                new = []
            return Polynomial(new)

    def dot(self,S):
        """ This returns the sum of ck*S{N-k} where N+1 = len(S),
            and k runs from 0 to m-1 (m is my degree)
        """
        m = len(self)
        N = len(S)
        C = self[:-1]
        S = S[N-m+1:]
        return dot(C,S)

    def __mul__(self,other):
        deg = len(self) + len(other) - 2
        prod = [0]*(deg + 1)
        for k,x in enumerate(self):
            for j,y in enumerate(other):
                prod[k+j] ^= (x&y)
        return Polynomial(prod)

    def __pow__(self,ex):
        if ex==0:
            return Polynomial([1])
        else:
            return self*(self**(ex-1))


def dot(x, y):
        """Returns the dot product of two lists."""
        return reduce(xor, [a&b for (a,b) in zip(x,y)], 0)


X   = Polynomial([1, 0])
One = Polynomial([1])

def bm(seq):
    """Implementation of the Berlekamp-Massey algorithm, the purpose
       of which is to find a LFSR with the smallest possible length
       that generates a given sequence.

       A generator is returned  that yields the current LFSR at
       each call. At the k-th call the yielded LFSR is guaranteed
       to generate the first k bits of SEQ.

       Input :
       Output: A list of coefficients [c0, c1,..., c{m-1}]

       Internally, if the state of the LFSR is (x0,x1,...,x{m-1})
       then the output bit is x0, the register contents are shifted
       to the left, and the new
       x{m-1} = c0 * x0 + c1 * x1 +...+c{m-1} * x{m-1}

       The generating function G(x) = s_0 + s_1 * x^1 + s_2 * x^2 + ...
       of a LFSR is rational and (when written in lowest terms) the
       denominator f(x) is called the characteristic polynomial of the
       LFSR. Here we have f(x) = c0 * x^m + c1 * x^{m-1} +...+ c{m-1} * x + 1.
       """
    # Allow for an input string along with a list or tuple
    if type(seq) == type('string'):
        seq = list(map(int, tuple(seq)))

    m = 0

    # N is the index of the current element of the sequence SEQ under consideration
    # f is the characteristic polynomial of the current LFSR
    N,f = 0,One

    # N0 and f0 are the values of N and f when m was last changed
    # N0 starts out as -1
    N0,f0 = -1,One

    n = len(seq)
    while N < n:
        # Does the current LFSR compute the next entry in the
        # sequence correctly? If not we need to update the LFSR
        if seq[N] != f.dot(seq[:N]):
            # If N is small enough we can get away with just
            # updating the coefficients in the LFSR. Note that
            # the 'X' occuring below is a global variable and
            # is the indeterminant in the polynomials defined
            # by the class 'Polynomial'. That is, X=Polynomial([1,0])
            if 2*m>N:
                f = f + f0 * X**(N-N0)

            # Otherwise we'll have to update everything
            else:
                f0, f = f, f + f0 * X**(N-N0)
                N0 = N
                m = N+1-m

        # Next element..
        N += 1

        # yield the coefficients [c0, ... , c{m-1}] of the
        # current LFSR's feedback function
        yield f[:-1]
    # yield the final LFSR coefficients once again
    yield f[:-1]

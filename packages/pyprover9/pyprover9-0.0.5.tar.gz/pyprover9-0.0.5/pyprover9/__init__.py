print( "* pyprover9 by Brandon Bennett (Sept 2023)" )
print( "* a Colab front-end for Prover9 by William McCune")

from .pyprover9 import prove, input, full_output

import os

def template(fname):
    d = os.path.dirname(__file__)
    respath = os.path.join( d, "problems", fname )
    with open( respath ) as f:
        content = f.read()
    return content



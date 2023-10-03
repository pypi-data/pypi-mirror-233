print( "* pyprover9 by Brandon Bennett (Sept 2023)" )
print( "* a Colab front-end for Prover9 by William McCune")
print( "Version date: 2023.10.02")
print()
print( """Provides:
  pyprover9.prove( assumptions, goal )
  pyprover9.input( p9inputString )
  pyprover9.full_output()   
  pyprover9.p9file( assumptions, goal )
  pyprover9.p9download( assumptions, goal )
  pyprover9.template( "probset/probname.p9" )
""" )

from .pyprover9 import prove, input, full_output, p9file
import os

def template(fname):
    d = os.path.dirname(__file__)
    respath = os.path.join( d, "problems", fname )
    with open( respath ) as f:
        content = f.read()
    return content


from google import colab
def p9download( assumptions, goal, fname, template = None ):
    content = p9file( assumptions, goal, template=template )
    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    if not fname.endswith('.p9'):
      fname += ".p9"
    path = os.path.join( 'tmp', fname )
    with open( path, "w") as f:
          f.write(content)
    colab.files.download(path)
    

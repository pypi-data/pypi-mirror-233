from setuptools import setup, find_packages

setup (
  name='pygments-epsilon',
  version='1.0',
  description='Pygments lexer for Epsilon languages suite.',
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  license='MIT',
  
  author='Abdul Nafey Mohammed',
  
  url='https://github.com/iNafey/pygments-epsilon',
  
  packages=find_packages(),
  entry_points =
  """
  [pygments.lexers]
  etl = lexer:EtlLexer
  eol = lexer:EolLexer
  emfatic = lexer:EmfaticLexer
  """,
  
  classifiers=[
        'Environment :: Plugins',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
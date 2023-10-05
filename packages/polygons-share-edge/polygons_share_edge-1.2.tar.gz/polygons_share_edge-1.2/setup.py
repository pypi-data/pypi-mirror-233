from distutils.core import setup, Extension

polygon_module = Extension('polygons_share_edge',
                           sources = ['src/polygons_share_edge/polygons_share_edge.cpp'])

long_description = """A CPython extension which checks two polygons
for any shared edge vector.
"""

setup (name = 'polygons_share_edge',
       version = '1.2',
       description = 'CPython extension for checking if two polygons share an edge.',
       url = 'https://github.com/sgaebel/polygon_edges',
       author = 'Dr. Sebastian M. Gaebel',
       author_email = 'gaebel.sebastian@gmail.com',
       license = 'MIT',
       ext_modules = [polygon_module],
       long_description = long_description,
       classifiers = [
              'Development Status :: 5 - Production/Stable',
              'Intended Audience :: Developers',
              'Topic :: Scientific/Engineering :: Mathematics',
              'License :: OSI Approved :: MIT License',
              'Programming Language :: Python :: 3.10'],
       keywords = 'geometry polygon',
       python_requires = '>=3.10')

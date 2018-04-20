from distutils.core import setup

setup(name='WeightedObject',
      version='1.0.0',
      description='A pp system which accounts for the unfair length bonus in some maps.',
      author='MBmasher',
      author_email='mbmasher@gmail.com',
      packages=['main'],
	  requires=['numpy']
     )
from setuptools import setup

setup(name='jewelry-classify',
      version='0.1',
      description='Methods for image-based jewelry classification and inventory',
      url='http://TODO/this/later',
      author='Carlos Ezequiel',
      author_email='carlosezequiel@skyeyeproject.com',
      license='MIT',
      packages=['jc'],
      scripts=['bin/imagediff.py', 'bin/extractfeatures.py'],
      zip_safe=False)

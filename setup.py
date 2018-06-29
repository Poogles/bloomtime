from setuptools import setup

setup(name='bloomtime',
      version='0.1.1',
      description='Bloom filter with optional TTL',
      url='https://github.com/Poogles/bloomtime',
      author='Sam Pegler',
      author_email='sam@sampegler.co.uk',
      license='MIT',
      install_requires=["pyhash>=0.8.2"],
      packages=['bloomtime'],
      zip_safe=False)

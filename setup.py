from setuptools import setup, find_packages

setup(name='searchengine',
      version='0.1',
      description='A very simple search engine.',
      long_description='Student project',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Topic :: Text Processing :: General',
      ],
      keywords='search indexing',
      url='https://github.com/Neki/searchengine',
      author='Alizée Farshian, Benoît Faucon',
      author_email='faucon.benoit@cegetel.net',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      test_suite='nose.collector',
      tests_require=['nose'],
      scripts=['bin/searchengine'],
      install_requires=['matplotlib']
      )

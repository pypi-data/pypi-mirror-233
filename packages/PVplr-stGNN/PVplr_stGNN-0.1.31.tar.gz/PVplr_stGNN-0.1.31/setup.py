from setuptools import setup, find_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name="PVplr_stGNN",
      version="0.1.31",
      description="PV Performance Loss Rate Estimation using Spatio-temporal Graph Neural Networks",
      long_description=long_description,
      long_description_content_type='text/markdown',
      author="Yangxin Fan, Xuanji Yu, Raymond Wieser, Yinghui Wu, Roger French",
      author_email="yxf451@case.edu, xxy530@case.edu, rxw497@case.edu, yxw1650@case.edu, rxf131@case.edu",
      platforms=["any"],  # or more specific, e.g. "win32", "cygwin", "osx"
      packages=find_packages(),
      install_requires=[
          "pandas",
          "numpy",
          "scikit-learn",
          "scipy",
          "torch",
          "tensorflow",
          "keras",
          "torch-geometric"
      ],
      extras_require={
          "dev": [
              "setuptools",
              "wheel",
              "pytest"
          ]
      },
      entry_points={
          'console_scripts': [
              'pct3=PVplr_stGNN:hdfs',
          ],
      },
    # BSD 3-Clause License:
    # - http://choosealicense.com/licenses/bsd-3-clause
    # - http://opensource.org/licenses/BSD-3-Clause
    license='BSD License (BSD-3)',
    include_package_data=True,
)
from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r") as f:
  long_description = f.read()

setup(name='SupyCool',  # 包名
      version='1.0.2',  # 版本号
      description="It's SuperCool!",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='PythonHaveNoName',
      author_email='pythonhavenoname@qq.com',
      url='https://bbs.hezhongkj.top/SupyCool',
      install_requires=['pywin32'],
      license='GNU General Public License v3.0',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Topic :: Software Development :: Libraries'
      ],
      )

from setuptools import setup
import re


def version():
    with open('slidefit.py') as f:
        version_file = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(description='Fit images into slides',
      author='Tomas Nordin',
      author_email='tomasn@posteo.net',
      license='GPLv3+',
      classifiers=[
          'Programming Language :: Python :: 3',
          'Environment :: Console',
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Operating System :: OS Independent',
          'Topic :: Documentation',
          'Topic :: Office/Business',
          'Topic :: Utilities',
          'Topic :: Multimedia :: Graphics :: Presentation'
      ],
      entry_points={
          'console_scripts': 'slidefit=slidefit:distmain'
      },
      install_requires=['python-pptx>=0.6.22', 'docopt'],
      py_modules=['slidefit'],
      keywords='slides presentation image productivity tool pptx',
      long_description=open('README.rst').read(),
      long_description_content_type='text/x-rst',
      name='slidefit',
      url='https://github.com/tomnor/slidefit',
      version=version(),)

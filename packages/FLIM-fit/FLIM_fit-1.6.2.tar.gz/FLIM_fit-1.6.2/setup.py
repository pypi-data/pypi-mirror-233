from distutils.core import setup
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
  name='FLIM_fit',
  packages= ['FLIM_fit'],
  version='1.6.2',
  license='Walsh Lab',
  description='This GUI performs fluorescence lifetime decay analysis at cellular level.',
  author='Linghao Hu',
  author_email='hulinghao@tamu.edu',
  keywords=['Fluorescence Lifetime', 'Decay Analysis', 'Cell-Level'],
  long_description=long_description,
  long_description_content_type="text/markdown",
  package_data={'FLIM_fit': ['*.h5']},
  install_requires=[
      'customtkinter',
      'numpy',
      'pandas',
      'scikit-learn',
      'CTkMessagebox',
      'scipy',
      'matplotlib',
      'tifffile',
      'tensorflow',
      'openpyxl',
      'sdtfile'
  ],
  classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',
      'License :: OSI Approved :: BSD License',
      'Programming Language :: Python :: 3',
  ],
  entry_points={
      'console_scripts': [
          'flimfit=FLIM_fit.GUI:run_gui',
      ],
  },
)

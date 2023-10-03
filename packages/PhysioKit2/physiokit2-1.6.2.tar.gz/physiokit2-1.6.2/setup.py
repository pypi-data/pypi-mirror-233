from setuptools import setup

setup(name='PhysioKit2',
      version='1.6.2',
      description="PhysioKit is a novel physiological computing toolkit which is open-source, accessible and affordable. HCI hobbyists and practitioners can easily access physiological sensing channels that help monitor our physiological signatures and vital signs including heart rate, heart rate variability, breathing rate, electrodermal activities. The toolkit works with a low-cost micro-controller such as Arduino. Currently, it supports acquiring EDA, Resp and PPG using any low-cost Arduino board.",
      url='https://github.com/PhysiologicAILab/PhysioKit',
      author=['Jitesh Joshi', 'Katherine wang', 'Youngjun Cho'],
      author_email='youngjun.cho@ucl.ac.uk',
      license='MIT',
      packages=['PhysioKit2'],
      install_requires=[
        'matplotlib',
        'neurokit2',
        'numpy',
        'opencv_contrib_python',
        'pyserial',
        'PySide6',
        'PySide6',
        'PySide6_Addons',
        'PySide6_Essentials',
        'scipy',
        'setuptools'
      ],
      include_package_data=True,
      package_dir={"": "src"},
      package_data={"": ["*.png"]},
      zip_safe=True
      )
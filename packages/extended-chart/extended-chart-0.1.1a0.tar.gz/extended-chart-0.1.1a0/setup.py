from setuptools import setup

setup(name='extended-chart',
      version='0.1.1a',
      description='wrapper for lightweight-charts-python for trading strategy discovery',
      url='https://github.com/karunkrishna/poc_lightweight_charts',
      author='Karun Krishna',
      author_email='karun.krishna@amce.corp',
      license='MIT',
      packages=['extended_chart'],
      install_requires=['lightweight-charts'],
      zip_safe=False
      )

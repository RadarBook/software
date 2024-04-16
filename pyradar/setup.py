from setuptools import setup

setup(name='RadarBook',
			version='0.1',
			description='Accompanying software for Introduction to Radar using Python and MATLAB',
			url='https://github.com/RadarBook/',
			author='Lee A. Harrison',
			author_email='pythonradarbook@gmail.com',
			license='',
      			packages=['Chapter01','Chapter02','Chapter03','Chapter04','Chapter05','Chapter06','Chapter07','Chapter08','Chapter09','Chapter10','Chapter11','Libs'],
			zip_safe=False,
            install_requires=[
                'numpy',
                'scipy',
                'matplotlib',
                'pyqt5',
			])

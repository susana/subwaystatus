from setuptools import setup

setup(
    name='subwaystatus',
    version='0.1',
    description='Provides MTA subway status',
    url='http://github.com/susana/subwaystatus',
    author='Susana C Delgadillo',
    license='MIT',
    packages=['subwaystatus'],
    zip_safe=False,
    entry_points = {
        'console_scripts': ['subwaystatus=subwaystatus.subwaystatus:main'],
    },
    install_requires=[
        'APScheduler==3.3.1',
        'arrow==0.10.0',
        'beautifulsoup4==4.6.0',
        'python-dateutil==2.6.0',
        'pytz==2017.2',
        'requests==2.20.0',
        'six==1.10.0',
        'tzlocal==1.4',
    ]
)

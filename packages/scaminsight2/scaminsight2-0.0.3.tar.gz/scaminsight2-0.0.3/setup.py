from setuptools import setup, find_packages

setup(
    name='scaminsight2',
    version='0.0.3',
    description='PYPI tutorial package creation written by',
    author='tester',
    license="MIT",
    author_email='tester@gmail.com',
    url='https://github.com/test',
    install_requires=['python-whois',  'bs4', 'selenium'],
    packages=find_packages(exclude=[]),
    keywords=[''],
    python_requires='>=3.6',
    scripts=['scaminsight/main.py'],
    entry_points={
        'console_scripts': [
            'scaminsight2test=scaminsight.main:main'
        ]
    },
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

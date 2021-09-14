from setuptools import setup


requires = ["numpy",
			"pandas",
			"jpholiday",
			"investpy"]


setup(
    name='ytrader',
    version='0.1',
    description='Templete classes for system trader.',
    url='https://github.com/YONDE927/ytrader',
    author='yonde1202(Yuta Harada)',
    author_email='svyuta1202@gmail.com',
    license='MIT',
    keywords='trade trading finance',
    packages=[
        "ytrader"
    ],
    install_requires=requires,
    classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Financial and Insurance Industry',
		'Topic :: Office/Business :: Financial :: Investment',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
	python_requires='>=3.6, <4',
)
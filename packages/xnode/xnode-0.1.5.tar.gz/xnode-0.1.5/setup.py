from setuptools import setup, find_packages

setup(
    name='xnode',
    version='0.1.5',
    description='xnode written by PlanXStudio',
    author='devcamp',
    author_email='devcamp@gmail.com',
    url='https://github.com/planxstudio/xnode',
    install_requires=['click', 'python-dotenv', 'pyqt5', 'PythonQwt', 'pyserial'],
    packages=find_packages(exclude=[]),
    keywords=['micropython', 'zigbee', 'xnode', 'pypi'],
    python_requires='>=3.8',
    package_data={},
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'xnode = xnode.xnode:main',
            'xmon = xnode.xmon:main',            
        ],
    },
)

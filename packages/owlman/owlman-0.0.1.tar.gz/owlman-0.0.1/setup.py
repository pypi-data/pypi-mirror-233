from setuptools import setup, find_packages

setup(
    name='owlman',
    version='0.0.1',
    description='금융 분석을 위한 툴 모음',
    author='qus0in',
    author_email='qus0in@gmail.com',
    url='https://github.com/qus0in/owlman',
    install_requires=['requests', 'pandas',],
    packages=find_packages(exclude=[]),
    keywords=['owlman'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
)
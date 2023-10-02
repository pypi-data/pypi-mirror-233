from setuptools import setup, find_packages

setup(
    name='teqoa-water-use-equations',
    version='0.1',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'pandas',
        'requests',
        'numpy'
        # List your project dependencies here, for example:
        # 'numpy>=1.18',
    ],
    author='Munyaradzi Mandava',
    author_email='info@teqoa.biz',
    description='A package for water use equations.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mandavamunya/teqoa-water-use-equations',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)

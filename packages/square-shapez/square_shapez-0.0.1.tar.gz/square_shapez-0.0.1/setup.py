from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='square_shapez',
    version='0.0.1',
    author='reducter',
    author_email='example@gmail.com',
    description='This is module to calculate shapes area.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/Similization/ShapeAreaLib',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='shapes area ',
    project_urls={
        'GitHub': 'https://github.com/Similization/ShapeAreaLib'
    },
    python_requires='>=3.6'
)

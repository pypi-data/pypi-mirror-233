from setuptools import setup
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cemir-print',
    version='202231003.1',
    description='A colorful printing library for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='muslu yüksektepe',
    author_email='musluyuksektepe@gmail.com',
    url='https://github.com/muslu/cemir_print',
    packages=['cemir_print'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)

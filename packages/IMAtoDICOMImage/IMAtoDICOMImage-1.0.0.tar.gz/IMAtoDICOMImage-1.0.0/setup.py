from setuptools import setup, find_packages


with open('README.txt', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='IMAtoDICOMImage',
    version='1.0.0',  # Replace with your library version
    description='IMA converter',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Maryam Oghbaei',
    author_email='maryam.oghbayi@gmail.com',
    url='',  # Replace with your repository URL
    packages=find_packages(),
    install_requires=[
        'pydicom',
        'numpy',
        'matplotlib',
        'Pillow',
        'imageio',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

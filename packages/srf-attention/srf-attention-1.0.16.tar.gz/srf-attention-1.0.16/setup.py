from setuptools import setup, find_packages

setup(
    name='srf-attention',
    version='1.0.16',
    packages=find_packages(),
    author='Alex Levenston',
    author_email='alexlevenston2021@gmail.com',
    description='Simplex random feature attention in PyTorch for both training and inference',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/alexjlevenston/srf-attention',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'torch',
        'scipy',
        'einops'
    ],
    include_package_data=True,
    python_requires='>=3.6',
)



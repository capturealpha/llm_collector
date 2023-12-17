from setuptools import setup, find_packages

setup(
    name='llm_collector',
    version='0.1.0',
    author='thealpha0ne',
    author_email='smeredithi@capturealpha.com',
    description='Django file content extractor for big token llm models',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/capturealpha/llm_collector',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'llm_collector=llm_collector:main',
        ],
    },
    install_requires=[
        # List your project's dependencies here
        # e.g., 'requests', 'Django>=3.0',
        'termcolor',  # If termcolor is a dependency
    ],
    classifiers=[
        # Classifiers help users find your project by categorizing it
        # For a list of valid classifiers, see https://pypi.org/classifiers/
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

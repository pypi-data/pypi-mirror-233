from setuptools import setup, find_packages

# Read the contents of your README.md file
with open("readme.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name='qs-files',
    version='1.5.0.0.0.1',
    description='Python library for managing .qs files and configurations.',
    author='Quadrat.Ik',
    author_email='quadrat.ik@yandex.com',
    url='https://github.com/QuadratNew/qs-files',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Russian',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
)
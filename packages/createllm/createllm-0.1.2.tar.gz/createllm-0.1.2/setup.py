from setuptools import setup, find_packages

VERSION = '0.1.2' 
DESCRIPTION = 'Python package that let you create own transformers based models on your own data'
LONG_DESCRIPTION = 'Python package that let you create own transformers based models on your own data'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="createllm", 
        version=VERSION,
        author="Khushal Jethava",
        author_email="Khushaljethava14@outlook.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        url='https://github.com/khushaljethava/createllm',
        packages=find_packages(),
        install_requires=['dill','torch','torchvision'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
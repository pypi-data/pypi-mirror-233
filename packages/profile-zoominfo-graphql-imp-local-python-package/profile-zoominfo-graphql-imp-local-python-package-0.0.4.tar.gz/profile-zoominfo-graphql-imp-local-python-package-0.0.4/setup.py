import setuptools
# Each Python project should have pyproject.toml or setup.py
# TODO: Please create pyproject.toml instead of setup.py (delete the setup.py)
# used by python -m build
# ```python -m build``` needs pyproject.toml or setup.py
# The need for setup.py is changing as of poetry 1.1.0 (including current pre-release) as we have moved away from needing to generate a setup.py file to enable editable installs - We might able to delete this file in the near future
setuptools.setup(
     # TODO: Please update the name and delete this line i.e. XXX-local or XXX-remote (without the -python-package suffix). Only lower case
     name='profile-zoominfo-graphql-imp-local-python-package',  
     # TODO: Please update the URL bellow
     version='0.0.4', # https://pypi.org/project/profile-zoominfo-graphql-imp-local-python-package/
     author="Circles",
     author_email="sahar.g@circ.zone",
     # TODO: Please update the description and delete this line
     description="PyPI Package for Circles profile-zoominfo-graphql-imp-local-python-package Local/Remote Python",
     # TODO: Please update the long description and delete this line    
     long_description="This is a package for sharing common XXX function used in different repositories",
     long_description_content_type="text/markdown",
     url="https://github.com/circles",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: Other/Proprietary License",
         "Operating System :: OS Independent",
     ],
 )

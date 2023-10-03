import setuptools

setuptools.setup(
    name='dataflow_xent',
    description='Package to be used inside cross entropy beam pipeline',
    version='0.0.3',
    install_requires=['oauth2client', 'google-cloud-bigquery', 'pandas', 'db-dtypes', 'scikit-learn'],
    packages=setuptools.find_packages(),
    python_requires=">=3.7, <4"
 )
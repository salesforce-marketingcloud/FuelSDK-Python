from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(
    version='1.3.1',
    name='Salesforce-FuelSDK',
    description='Salesforce Marketing Cloud Fuel SDK for Python',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='ExactTarget',
    py_modules=['ET_Client'],
    python_requires='>=3',
    packages=['FuelSDK'],
    url='https://github.com/salesforce-marketingcloud/FuelSDK-Python',
    license='MIT',
    install_requires=[
        'pyjwt>=1.5.3',
        'requests>=2.18.4',
        'suds-community>=0.7',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3.7',
    ],
)
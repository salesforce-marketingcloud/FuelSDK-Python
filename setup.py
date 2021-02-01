from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(
    version='1.3.1',
    name='Fever-FuelSDK',
    description='Fever Salesforce Marketing Cloud Fuel SDK for Python',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Feverup',
    py_modules=['ET_Client'],
    packages=['FuelSDK'],
    url='https://github.com/Feverup/FuelSDK-Python',
    license='MIT',
    install_requires=[
        'pyjwt>=1.5.3',
        'requests>=2.18.4',
        'suds-jurko==0.6',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3.3',
    ],
)

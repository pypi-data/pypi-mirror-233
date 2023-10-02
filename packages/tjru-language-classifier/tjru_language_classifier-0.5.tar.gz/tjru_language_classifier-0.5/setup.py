from setuptools import setup, find_packages

setup(
    name='tjru_language_classifier',
    version='0.5',
    packages=find_packages(),
    install_requires=[
        'scikit-learn',
        'joblib'
    ],
    package_data={
        'tjru_language_classifier': ['model.pkl'],
    },
    author='Sobir Bobiev',
    description='A simple tajik-russian language classifier',
)

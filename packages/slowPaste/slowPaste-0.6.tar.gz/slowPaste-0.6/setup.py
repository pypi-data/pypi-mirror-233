from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='slowPaste',
    version='0.6',
    packages=find_packages(),
    install_requires=[
        'pyperclip',
        'pyautogui',
        'keyboard'
    ],
    license='MIT',
    description='A Python package to simulate human-like typing with adjustable speed.',
    author='Robbie Walmsley',
    author_email='robbiebusinessacc@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/robbiebusinessacc',  
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

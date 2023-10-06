from setuptools import setup, find_packages




# Project metadata
name = 'afrinet_system'
version = '0.0.1'
description = 'A brief description of your project'
long_description = 'A longer description of your project'
author = 'Your Name'
author_email = 'your.email@example.com'

# Package dependencies (add your project-specific dependencies here)
install_requires = [
    'requests',
    'numpy',
    'pandas',
    # Add more dependencies as needed
]

# License information
license = 'MIT'

# Additional classifiers for your package (customize as needed)
classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

# Entry point scripts (if applicable)
entry_points = {
    'console_scripts': [
        'my_script = afrinet_system.module:main',
    ],
}

# Package information
packages = find_packages()

# Package setup
setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=author,
    author_email=author_email,
    url='https://github.com/yourusername/yourproject',  # Replace with your project's URL
    packages=packages,
    install_requires=install_requires,
    license=license,
    classifiers=classifiers,
    entry_points=entry_points,
)
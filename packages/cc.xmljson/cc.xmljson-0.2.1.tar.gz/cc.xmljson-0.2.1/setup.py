import setuptools

with open("README.rst", "r", encoding="utf-8") as readme_file:
    readme = readme_file.read()
    
with open("HISTORY.rst", "r", encoding="utf-8") as history_file:
    history = history_file.read().replace(".. :changelog:", "")

setuptools.setup(
    name="cc.xmljson",
    version="0.2.1",
    author="Uncertainty.",
    author_email="t_k_233@outlook.email",
    description="Converts XML into JSON/Python dicts/arrays and vice-versa.",
    license="MIT",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/uncertainty-cc/xmljson-Python",
    project_urls={
        
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)

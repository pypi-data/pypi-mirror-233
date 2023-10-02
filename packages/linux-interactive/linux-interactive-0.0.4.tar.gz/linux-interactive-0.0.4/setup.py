from setuptools import setup

# Package description
package_description = (
    "Linux Interactive is a utility that interacts with the OpenAI GPT-4 model to provide Linux commands based on user prompts."
)

setup(
    name="linux-interactive",
    version="0.0.4",
    py_modules=["linux_interactive"],
    install_requires=[
        "openai>=0.28.0",
    ],
    entry_points={
        "console_scripts": [
            "li=linux_interactive:main",
        ],
    },
    description="Linux Interactive: Interactive Linux Commands with OpenAI GPT-4",
    long_description=package_description,
    long_description_content_type="text/plain",
    url="https://github.com/ktamulonis/li",
    author="Kurt Tamulonis",
    author_email="kurttamulonis@gmail.com",
)


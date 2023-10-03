"""
   $$\       $$\ $$\           $$$$$$\             $$\                         
  $$  |     $$  |\$$\         $$  __$$\            $$ |                        
 $$  /     $$  /  \$$\        $$ /  \__| $$$$$$\ $$$$$$\   $$\   $$\  $$$$$$\  
$$  /     $$  /    \$$\       \$$$$$$\  $$  __$$\\_$$  _|  $$ |  $$ |$$  __$$\ 
\$$<     $$  /     $$  |       \____$$\ $$$$$$$$ | $$ |    $$ |  $$ |$$ /  $$ |
 \$$\   $$  /     $$  /       $$\   $$ |$$   ____| $$ |$$\ $$ |  $$ |$$ |  $$ |
  \$$\ $$  /     $$  /        \$$$$$$  |\$$$$$$$\  \$$$$  |\$$$$$$  |$$$$$$$  |
   \__|\__/      \__/          \______/  \_______|  \____/  \______/ $$  ____/ 
                                                                     $$ |      
                                                                     $$ |      
                                                                     \__|      
"""
from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="tgbotstat",
    version="1.0.0",
    author="Coding Team",
    author_email="codingteam@telegmail.com",
    description="Un outil pour suivre les statistiques d'utilisation des commandes d'un bot Telegram.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/codingtuto/tgbotstat",
    packages=["tgbotstat"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

# Packetizer 📦

Hello 👋, welcome to the Packetizer repository, your go-to tool for keeping your Python code neat and tidy.

## What Does Packetizer Do?

Imagine working on a large Python project and you find your `module.py` file has become a monolith with thousands of lines and dozens of classes. Enter Packetizer, your life-saver.

With a single command, Packetizer takes that behemoth of a file, splits it into multiple files based on the classes, and even generates an `__init__.py` so it all works like a proper Python package. 🎉

## 🛠️ Installation

To install Packetizer, simply run:

```bash
pip install packetizer
```

## 🚀 Quick Start

Assuming you have a `module.py` full of classes, just run:

```bash
packetizer module.py
```

Voilà, you'll get a folder named `module` with each class in its own `.py` file and an `__init__.py` tying it all together as a package.

## 📜 Features

- Automatically splits classes into their own files
- Generates an `__init__.py` so it functions as a package
- Option to remove unused imports
- User-friendly and easy to use


## 🤝 Contributing

We'd love to see your contributions and make Packetizer even better. Feel free to open an issue or make a pull request.

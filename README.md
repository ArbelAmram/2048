# Python 2048 Game with Pygame

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.1-green.svg)
![License](https://img.shields.io/badge/license-MIT-black.svg)

### Overview
This project is a Python implementation of the popular 2048 game using the Pygame library for the graphical interface.</br> 
The goal of the game is to combine numbered tiles on a grid to create a tile with the number 2048. </br>
The game includes intuitive controls and a graphical interface built with Pygame, offering a fun and interactive experience for players. </br>
Dive into the world of 2048 and challenge yourself with this Python implementation!</br>

#### Video Demonstration

Watch a demo of the project [here](https://github.com/arbelamram/2048/assets/51449659/b3046508-d94f-406c-91e1-7957a5153954)


## Table of Contents
- [Project Description](#project-description)
  - [Technologies and tools](#technologies-and-tools)
  - [Object-Oriented Programming (OOP)](#object-oriented-programming-oop)
- [Usage](#usage)
  - [Getting Started](#getting-started)
  - [Running the Application](#running-the-application)
  - [Testing](#testing)
- [Additional Information](#additional-information)
  - [Contributing](#contributing)
  - [Contact](#contact)
  - [Acknowledgments](#acknowledgments)
  - [License](#license)

## Project Description

### Technologies and tools
- **Programming Language:** Python
- **Library:** Pgame
- **Testing:** Unittest

### Object-Oriented Programming (OOP)
- **Encapsulation:**
  The `Game` class encapsulates all the game-related attributes and methods that help in managing the game state and behavior.
  
- **Modularity:**
  The code is divided into several methods within the `Game` class, each responsible for a specific functionality. This modularity improves code readability, maintainability, and reusability.

- **Abstraction:**
  The `Game` class provides a high-level interface for managing the game, hiding the complex implementation details.

- **Inheritance and Composition:**
  The `Game` class uses instances of the `Tile` class, demonstrating composition. The `Tile` objects are stored in `tiles_dict` and are manipulated through various game methods. This allows for more complex behavior by combining simpler objects.

## Usage

### Getting Started

1. **Prerequisites**:
    * Python 3.12+
    * `pip` (Python package installer)

2. **Clone the Repository**:
    ```sh
    git clone <repository-url>
    ```

3. **Create a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  
    ```
    * On Windows use:
    ```sh
    venv\Scripts\activate
    ```

4. **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

### Running the Application

1. **Start the Game**:
    ```sh
    python main.py
    ```

2. **Controls**:
    * Use the arrow keys to move the tiles.
    * Combine tiles with the same number to merge them and score points.
    
3. **Objective**:
    Reach the 2048 tile to win the game.

### Testing
* **Unit Testing:** Unittest for Python

#### How to Run the Tests
1. **Install Dependencies**:
The unittest module is included in the Python standard library, so you do not need to install it separately. It is available out-of-the-box in any standard Python installation.
To use unittest, simply import it in your test files:
    ```sh
    import unittest
    ```

2. **Run the Tests**: To run the tests, use the following commands:
    ```sh
    python -m unittest discover -v
    ```

## Additional Information

### Contributing
Contributions to the project are welcome.</br>
Please fork the repository, create a feature branch, and submit a pull request for review.

### Contact

If you have any questions or suggestions, feel free to reach out:

- Email: [ArbelAmram@github.com](mailto:arbelamram@github.com)

### Acknowledgments

- Resources: [Badges](https://img.shields.io)

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

# Infinity Scrape

Have you ever wanted to create anime or honey or anything else in [Infinity Craft](https://neal.fun/infinite-craft/), but didn't know how? With this repository, now you can...

Also there is already something like this as a [discord bot](https://discord.gg/3H2YBfxVxx).

## Installation

Also someone made a [tutorial for windows](https://www.youtube.com/watch?v=WRgj4NRL2hA). 

### Step 1: Install Python

Before you can use the Infinity Scrape, you need to have Python installed on your system. Follow these steps to install Python:

1. Open your web browser and navigate to the [Python download page](https://www.python.org/downloads/).
2. Download the latest version of Python for Windows.
3. Once the download is complete, run the installer.
4. Follow the on-screen instructions to complete the installation process, ensuring that you select the option to add Python to your system PATH.

### Step 2: Install Git

Before you can clone the repository, you need to have Git installed on your system. Git is a version control system that allows you to manage and track changes to files. Follow these steps to install Git:

1. Open your web browser and navigate to the [Git download page](https://git-scm.com/downloads).
2. Download the latest version of Git for Windows.
3. Once the download is complete, run the installer.
4. Follow the on-screen instructions to complete the installation process, ensuring that you select the appropriate options for your system.

### Step 3: Clone the Repository

Now that Python and Git are installed, you can clone the Infinity Scrape repository to your local machine. Follow these steps:

1. Open the Command Prompt by pressing `Win + R`, typing `cmd`, and then pressing `Enter`.
2. Navigate to the directory where you want to clone the repository using the `cd` command. For example:

    ```bash
    cd C:\Projects
    ```

3. Clone the repository by running the following command:

```bash
git clone https://github.com/admin-else/infinity-scrape
```

4. Once the cloning process is complete, navigate into the cloned directory:

```bash
cd infinity-scrape
```

### Step 4: Install Python Dependencies

Infinity Scrape relies on certain Python libraries to function (its just requests). You can install these dependencies using the following command:

```bash
pip install -r requirements.txt
```

## Usage

Once you have installed everything, you can run:

```bash
python3 howtoget.py
```

This command will provide you with a list of items you need to craft for your desired item. However, if you encounter a message like:

```bash
$ python3 howtoget.py
what do you want: trolling
didn't find source of Trolling...
```

It means the source for your desired item is not found. In such a case, you need to run the scraper again until you find your desired word. You can do this with:

```bash
$ python3 scrape.py
```

If you do that, it would be appreciated if you could make a pull request so that other people don't have to repopulate the database if you alread did it.
If you have more problems you can contact me on [discord](https://discord.gg/w5t524meRT).

# Git Setup
## For Windows
1. Download Git for Windows: https://git-for-windows.github.io/
2. Generating an SSH key within Git Bash: https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/
3. Add the public SSH key generated to your GitHub account: https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/
4. Go the folder you want to clone the WANCom folder in, and type: `git clone git@gits-15.sys.kth.se:iaq/WANCom.git`
5. Type `cd WANCom` and then `dir` to check if the local folder matches the GitHub repo
You're set up!

## For MAC
1. Make sure git is installed on your computer. If it is not:
    - Make sure you're using the latest version of MAC OS and XCode
    - Add the path to the git command to your PATH: https://vandadnp.wordpress.com/2012/04/06/git-from-command-line-after-installing-xcode-on-os-x-lion/
2. Generate an SSH key: https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/#platform-mac
3. Add the public SSH key generated to your GitHub account: https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/#platform-mac
4. Go the folder you want to clone the WANCom folder in, and type: `git clone git@gits-15.sys.kth.se:iaq/WANCom.git`

## Linux
1. Make sure you have the `git` command available by running `which git` (if a path is returned, it's fine, otherwise you'll have to Google how to add the command to your system)
2. Generate an SSH key: https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/#platform-mac
3. Add the public SSH key generated to your GitHub account: https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/#platform-mac
4. Go the folder you want to clone the WANCom folder in, and type: `git clone git@gits-15.sys.kth.se:iaq/WANCom.git`

# Code review Setup
## MAC & Linux
Follow instructions here: https://kth.instructure.com/files/382495

## Windows
Follow instructions here: http://commondatastorage.googleapis.com/chrome-infra-docs/flat/depot_tools/docs/html/depot_tools_tutorial.html#_windows
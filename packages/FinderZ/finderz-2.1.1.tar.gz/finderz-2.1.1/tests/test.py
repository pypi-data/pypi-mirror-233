#!/usr/bin/env python3

import FinderZ

from FinderZ import GatherInfo as g

file_stats = g.computeHash("/Users/edwardferrari/MyPythonProjects/GitHubRepos/Active/Finderz/README.md")

print(file_stats)
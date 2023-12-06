# -*- coding: utf-8 -*-

class DiffModel:
    def __init__(self, repo=None, commit_files=None, diff_output=None):
        self.repo = repo
        self.commit_files = commit_files
        self.diff_output = diff_output

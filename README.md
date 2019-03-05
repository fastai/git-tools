# git-tools

Helper scripts and tools that improve productivity for git users.

Docs associated with these tools can be found [here](https://docs.fast.ai/dev/git.html).

## Index

- `hub-install.py`: A python script that automates the installation of hub tool based on your system platform. `hub` is a beginner-friendly tool that wraps the common git operations with simple commands. To learn more about using `hub`, see the [docs](https://hub.github.com/hub.1.html).

- `fastai-make-pr-branch`: This bash script will checkout a forked version of the original fastai repository, sync it with the original, create a new branch and set it up for a PR. **Windows users** need to use the `fastai-make-pr-branch-py` script, which currently requires the user to have a github token configured.
  
- `github-make-pr-branch`: Generic script to checkout a forked version of the original fastai repository, sync it with the original, create a new branch and set it up for a PR. (TODO: needs to be created from `fastai-make-pr-branch` and `fastai-make-pr-branch-py.)


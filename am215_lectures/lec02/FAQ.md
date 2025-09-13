# Git Lecture - Frequently Asked Questions

This document contains answers to common questions that may arise from the "Git Essentials & Workflow" lecture.

---

### Getting Started & Basic Workflow

#### Why do I have to `git add` files before I `commit`? What is the purpose of the staging area?
The staging area (or "index") lets you build a commit piece by piece. You might edit three files to fix a bug but also make an unrelated change in a fourth file. The staging area allows you to `add` only the three relevant files to create a focused, logical commit. This keeps your commit history clean and easy to understand.

#### What's the real difference between `git restore`, `git reset`, and `git revert`?
- **`git restore <file>`**: Discards changes in your *working directory* (uncommitted changes). Use this when you've made edits you want to throw away before committing.
- **`git revert <commit-hash>`**: Creates a **new commit** that undoes the changes from a previous commit. It's safe for shared history because it doesn't rewrite the past. Use this to undo a public, pushed commit.
- **`git reset --hard <commit-hash>`**: Moves the current branch pointer back to a previous commit, discarding all commits that came after it. It **rewrites history** and is dangerous for shared branches. Use it for local cleanup *before* you push.

#### If I add a file to `.gitignore` that I've already committed, why does Git keep tracking it?
`.gitignore` only prevents *untracked* files from being added to the repository. If a file is already being tracked (i.e., it was in a previous commit), Git will continue to monitor it. To stop tracking a file you've already committed, you must remove it from the index using `git rm --cached <file>`.

---

### Branching & Merging

#### When should I choose to `rebase` instead of `merge`?
- Use **`rebase`** on your *local, private branches* before merging them into a shared branch like `main`. This creates a cleaner, linear history that is easier to read.
- Use **`merge`** when combining work from *shared branches* or when you want to preserve the exact historical record of when branches diverged and were brought back together (the "diamond" shape in the history).

#### The slide says never to rebase shared branches. What actually happens if I do?
Rebasing rewrites commit history, creating new commit hashes. If you rebase a branch that others have already pulled, their history will diverge from the new, rebased history. When they try to pull updates, Git will see two different histories and force a messy merge, creating duplicate commits and confusion for the whole team.

#### What is a "fast-forward" merge?
A fast-forward merge happens when the branch you are merging into (`main`) has not had any new commits since you created your feature branch. Git can simply move the `main` branch pointer forward to point to the same commit as your feature branch. No new "merge commit" is needed because there are no divergent histories to combine.

#### What if I have multiple stashes? How can I see them or apply a specific one?
You can have a stack of stashes.
- `git stash list` shows all of them.
- `git stash apply stash@{2}` applies a specific stash from the list (in this case, the third one down).
- `git stash pop` applies the most recent one (`stash@{0}`) and removes it from the list.

---

### Remotes & Collaboration

#### Can you explain the difference between `git fetch` and `git pull` again?
- **`git fetch`** downloads the latest changes from the remote but **does not** integrate them into your local working branch. It only updates your remote-tracking branches (like `origin/main`).
- **`git pull`** does a `git fetch` *and then* immediately tries to merge the downloaded changes into your current local branch.
- Use `fetch` on its own when you want to see what changes have been made on the remote before merging them into your own work.

#### What is the difference between my `main` branch and the `origin/main` branch?
- **`main`** is your *local* branch. It's where you do your work and make commits.
- **`origin/main`** is a *remote-tracking* branch. It's a read-only pointer to the state of the `main` branch on the remote server (`origin`) the last time you fetched from it. It only moves when you `git fetch` or `git pull`.

#### In the fork and pull request workflow, what is `upstream` and how is it different from `origin`?
By convention:
- **`origin`** is your personal fork of the repository on GitHub. You have write access to it, so you can `push` your changes there.
- **`upstream`** is the original repository that you forked from. You typically only have read access, so you use it to `fetch` updates to keep your local `main` branch in sync with the original project.

#### Why is using SSH keys considered more secure or convenient than HTTPS with a token?
- **Convenience**: Once set up, you don't have to enter a username or token every time you interact with the remote.
- **Security**: SSH keys use strong cryptography. The private key never leaves your computer, so your credentials are not transmitted over the network, making it much harder to compromise than a password or token.

---

### Under the Hood & Advanced Topics

#### If Git stores a whole new "blob" every time a file changes, doesn't that use a lot of disk space?
Not as much as you'd think. Git is very efficient. It compresses objects and, more importantly, periodically runs a "garbage collection" (`git gc`) that packs objects into highly compressed "packfiles," where it can store just the differences (deltas) between similar files to save even more space.

#### What does "detached HEAD" mean in practical terms?
"Detached HEAD" means you have checked out a specific commit directly, rather than a branch. It's useful for inspecting old code. If you make a new commit in this state, it won't belong to any branch. To get back, you can simply switch to an existing branch (`git switch main`) or create a new branch from that point (`git switch -c new-feature-branch`).

#### If I accidentally delete a branch, are the commits gone forever?
No, not immediately. Deleting a branch only deletes the pointer. The commits themselves still exist. You can use `git reflog` to find the hash of the last commit that was on that branch and then restore it by creating a new branch at that commit: `git branch <branch-name> <commit-hash>`.

#### For `git bisect`, do I have to manually test the code each time?
You can automate it. If you have a script that tests your code and exits with code 0 for "good" and a non-zero code for "bad", you can run `git bisect run <your-test-script.sh>`. Git will then run the script automatically for each step.

#### How do I completely remove a file with sensitive data from the entire Git history?
This is an advanced operation that requires rewriting history. The standard tool for this is `git filter-branch` or the more modern, recommended tool `git-filter-repo`. These tools will go through every commit and remove the file, which will change the hashes of all subsequent commits. This is a destructive action, and after doing it, everyone on the team will need to re-clone the repository.

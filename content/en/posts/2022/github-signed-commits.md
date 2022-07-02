---
title: "Signed commits on GitHub"
description: |
    A quick tutorial on setting up signed commits for GitHub-hosted git repositories.
date: "2022-07-02"
category: tutorials
tags:
  - til
image: "/static/img/articles/github-signed-commits.jpeg"
image_caption: "The looks of signed commits on GitHub (2018)."
---

Recently I set up personal repositories on a work laptop, using a [separate git config](https://www.freecodecamp.org/news/how-to-handle-multiple-git-configurations-in-one-machine/). As I was configuring the "personal" git config, I couldn't remember how to enable signed commits for committing to GitHub-hosted repositories.

I do have an [old Tweet](https://twitter.com/florimondmanca/status/1041419801346887681) about this, but I figured I might as well turn this into a quick blog post.

Note: this is specific to GitHub, which has signed commits docs spread across multiple pages of their documentation. For reference, Gitlab has an [single-page guide](https://docs.gitlab.com/ee/user/project/repository/gpg_signed_commits/), which looks much easier to follow.

### Step 1: Generate GPG keys

On Linux:

```console
$ sudo apt install gnupg
$ gpg --gen-key
```

Fill in your name and email, optionally set a pass phrase.

### Step 2: Let git know

See this [GitHub docs page](https://docs.github.com/en/authentication/managing-commit-signature-verification/telling-git-about-your-signing-key):

```console
$ gpg --list-secret-keys --keyid-format=long <EMAIL>
```

Identify the `sec` line and grab thelong form, which begins after the slash `/`, eg:

```console
sec   rsa3072/<GPG_KEY_ID> 2022-07-02 [SC] [expires: 2024-07-01]
```

Add it to your global git config, at `~/.gitconfig`. For me, `/.gitconfig-florimondmanca` (my personal git config) now looks like this:

```ini
[user]
	name = florimondmanca
	email = <EMAIL>
	signingkey = <GPG_KEY_ID>
[commit]
	gpgsign = true
```

`commit.gpgsign = true` enables auto-signing of git commits.

### Step 3: Add GPG key to GitHub

Generate the GPG public key from the long form GPG key ID:

```console
$ gpg --armor --export <GPG_KEY_ID>
```

Copy the output, then [add it to your GitHub account](https://docs.github.com/en/authentication/managing-commit-signature-verification/adding-a-new-gpg-key-to-your-github-account).

Should be all set. Now try pushing a commit, and you should see that green "Verified" badge on commits or pull requests.

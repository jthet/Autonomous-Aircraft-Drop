# Autonomous-Aircraft-Drop

## Startup Instructions

Create your own fork of this repository to do work on. 

To add your work to this repository, create a PR from your fork's branch into the same branch on this repository.

### Branch Instructions

Use `git branch` to see what branch you are on:
```sh
jacksonthetford Autonomous-Aircraft-Drop $ git branch
  image-recognition-main
* main
  trajectory-main
```

Then use `git checkout <your-project-name>` to switch to the branch for your work:

``` sh
jacksonthetford Autonomous-Aircraft-Drop $ git checkout image-recognition-main
Switched to branch 'image-recognition-main'
Your branch is up to date with 'origin/image-recognition-main'.
jacksonthetford Autonomous-Aircraft-Drop $ git branch
* image-recognition-main
  main
  trajectory-main
```

If you don't have a branch locally that matches a remote branch do the following:

`git checkout -b <name-of-branch> origin/<name-of-branch>`


### Docker Instructions

Run the following:

```
$ docker run -d --rm --name app --entrypoint=sleep jthet/autonomous-aircraft-drop infinity
...
$ docker exec -it app bash
```



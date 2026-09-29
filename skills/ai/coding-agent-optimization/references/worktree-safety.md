# Worktree Safety

Load before creating, using or removing a Git worktree for a parallel lane. A worktree is a second
checkout that shares the repository's object store, so a careless cleanup can destroy another
session's work. These rules sit beside the destructive-command gate in `hooks/`, which blocks the
worst commands mechanically; the rules below cover the judgement the hook cannot make.

## 1. Ask before creating

Creating a worktree adds a directory and a branch the owner did not ask for. Ask for consent,
naming the path, the branch and the reason, unless the owner has already approved worktrees for
this task. In a repository where another executor may be working, prefer a plain branch-free
read-only lane over a new worktree.

## 2. Detect where you already are

Before creating one, check whether the session is already inside a linked worktree:

```bash
git rev-parse --git-dir
git rev-parse --git-common-dir
```

If the two paths differ, you are in a linked worktree. Do not nest another one inside it; work
from the main checkout or ask. `git worktree list` shows every checkout that shares the store.

## 3. Record provenance at creation

When you create a worktree, write down in the task record or handoff file:

- the path and branch;
- the commit it started from (full SHA);
- the session or task that created it;
- the date.

Without this record, nobody can later tell a worktree this session made from one a person made.

## 4. Clean up only what this session created

Remove a worktree only if the provenance record shows this session created it. Before removal:

1. Run `git -C <path> status --porcelain`.
2. If anything is uncommitted or untracked, stop and name the untracked and modified files to
   the owner. Do not decide for them.
3. Never use `--force` on `git worktree remove`, and never delete the directory by hand.
4. After removal, run `git worktree prune` only if the owner agrees, and record what was pruned.

A worktree someone else made is left alone, even if it looks abandoned. Report it instead.

## 5. Never hide a lane's result in a worktree

Work that exists only in a worktree is not done. Before the lane reports, its changes are either
merged into the agreed branch by the owner's process or listed with their worktree path in the
report, so the controller can find them.

## Quick checklist

- [ ] Consent recorded, or prior approval cited.
- [ ] `--git-dir` and `--git-common-dir` compared before creating.
- [ ] Provenance written: path, branch, start SHA, creator, date.
- [ ] Status checked before removal; untracked files named, not deleted.
- [ ] No `--force`; only this session's worktrees removed.

(Adapted from obra/superpowers, MIT, https://github.com/obra/superpowers, commit
8ca22dba9a94f28898bbce59f2537ff4d87c747d. Paraphrased; no text copied.)

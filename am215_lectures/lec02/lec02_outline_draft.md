# AM215 Git Lecture Outline (Refined Draft)

## I. Motivation (3 slides)
1. Disasters without VC  
2. Collaboration nightmares  
3. Git as the solution (distributed, fast, branching)  

## II. Getting Started (6 slides)
4. Install & configure Git (name, email)  
5. Clone existing repo / init new repo  
6. Repo structure: working dir / staging / .git  
7. Git stores snapshots, not diffs  
8. File lifecycle  
9. `.gitignore`  

## III. Basic Local Workflow (4 slides)
10. `add`, `commit`, `status`, `diff`  
11. Viewing history: `log`  
12. Undoing: `restore`, `reset`, `revert`  
13. Amending commits  

## IV. Branching & Merging (8 slides)
14. Commits form a graph  
15. Branch = pointer, HEAD = current position  
16. Creating & switching branches  
17. Example: feature branch workflow  
18. Merging: fast-forward  
19. Merging: merge commits  
20. Stashing work  
21. Intro to rebase (local use only)  

## V. Remotes & Collaboration (12 slides)
22. Local vs remote repos  
23. Adding remotes, clone = automatic remote  
24. SSH vs HTTPS auth  
25. SSH Keys: Public/Private Key concept
26. Generating SSH Keys
27. Adding public key to GitHub
28. Push, fetch, pull (differences explained)  
29. Merge conflicts  
30. Fork → clone → branch → push → PR workflow  
31. Rebase dangers on shared branches  
32. GitHub/GitLab features  
33. GitHub CLI basics  

## VI. Under the Hood (4 slides)
34. Objects: blobs, trees, commits  
35. Content-addressing with hashes  
36. References: branches, tags, HEAD  
37. Why this matters  

## VII. Debugging & Advanced (4 slides)
38. Searching history (`log --grep`)  
39. Bisect for bug hunting  
40. Reflog for recovery  
41. Detached HEAD  
42. Cherry-pick (brief)  

## VIII. Best Practices (3 slides)
43. Commit practices  
44. Branch hygiene  
45. Resources & next steps  

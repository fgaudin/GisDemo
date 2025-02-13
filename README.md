# Deployment process

## Set up Invoke settings

Copy invoke.yaml.example to invoke.yaml and set variables

## Create and define deploy key on Github

```
# on server

ssh-keygen -t ed25519 -C "email_used_for_commits@users.noreply.github.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

Add key from ~/.ssh/id_ed25519.pub to https://github.com/fgaudin/GisDemo/settings/keys

## Deploy

```
inv deploy <commit_sha>
```

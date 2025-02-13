# Deployment process

## Set host in invoke.yaml

```
host: user@hostname
```

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
inv deploy
```

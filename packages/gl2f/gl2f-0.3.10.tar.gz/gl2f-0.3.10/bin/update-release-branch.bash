if [[ $(git diff --stat) != '' ]]; then
	echo 'work tree is dirty. return'
	return
fi

git fetch

current=$(git branch --show-current)
tag=$(git tag | tail -1)
echo "latest tag: ${tag}"

git switch release
git reset --hard $tag
git push

git switch $current

#!/bin/bash
# github web hook
log="/var/www/cgi/githubwebhooks/log"

input=$(cat /dev/stdin)

type="${HTTP_X_GITHUB_EVENT}"

# tests
# echo "Content-Type: text/plain"
# echo ""
# env
# echo "${type}"
# echo "${input}"
# exit 0

if [ "${REQUEST_METHOD}" != "POST" ]; then
  echo "HTTP/1.0 400 Bad Request"
  echo ""
  echo "POST requests only :)"
  exit 1
fi

if [ -z "${input}" ]; then
  echo "HTTP/1.0 400 Bad Request"
  echo ""
  echo "no JSON data input supplied"
  exit 1
fi

hr="--------------------------------"

if [ "${type}" == "push" ]; then
  message=$(echo "${input}" | \
  jq -r '"\n"
  + "'"${hr}"'\n"
  + .head_commit.timestamp + "\n"
  + .pusher.name + " pushed " + (.commits | length | tostring) + " commit(s)" + "\n"
  + "to " + .repository.name + "\n"
  + "\n"
  + .head_commit.message + "\n"
  + "\n"
  + .compare')
elif [ "${type}" == "issue_comment" ]; then
  message=$(echo "${input}" | \
  jq -r '"\n"
  + "'"${hr}"'\n"
  + .comment.created_at + "\n"
  + .repository.name + "\n"
  + .comment.user.login + " commented on #" + (.issue.number | tostring) + "\n"
  + "\n"
  + .comment.body + "\n"
  + "\n"
  + .comment.url')
elif [ "${type}" == "create" ]; then
  message=$(echo "${input}" | \
  jq -r '"\n"
  + "'"${hr}"'\n"
  + .repository.pushed_at + "\n"
  + .sender.login + " created a " + .ref_type + "\n"
  + .ref + "\n"
  + "  on" + "\n"
  + .repository.name + "\n"
  + "\n"
  + .repository.html_url + "/tree/" + .ref')
elif [ "${type}" == "pull_request" ]; then
  message=$(echo "${input}" | \
  jq -r '"\n"
  + "'"${hr}"'\n"
  + .pull_request.created_at + "\n"
  + .pull_request.user.login + " created pull request " + (.number | tostring) + "\n"
  + "\n"
  + .pull_request.title + "\n"
  + "\n"
  + .pull_request.body + "\n"
  + "\n"
  + .pull_request.url + "\n"')
else
  echo "HTTP/1.0 501 Not Implemented"
  echo ""
  if [ -z $type ]; then
    echo "No GitHub event (X-GITHUB-EVENT) header specified"
  else
    echo "GitHub event <${type}> is not implemented"
  fi
  exit 1
fi

if [ ! -e "/dev/usb/lp0" ]; then
  echo "HTTP/1.0 503 Service Unavailable";
  echo ""
  echo "Printer not plugged in"
  exit 1
fi

printf "${message}" > /dev/usb/lp0
printf "\n\n\n\n" > /dev/usb/lp0

echo "Content-Type: text/plain"
echo ""
echo "printed <${type}> event:"
echo ""
echo "${message}"

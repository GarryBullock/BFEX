#!/bin/bash
# RunCommand() {
#   typeset cmnd="$*"
#   typeset ret_code

#   echo cmnd=$cmnd
#   eval $cmnd
#   ret_code=$?
#   return ret_code
# }

# command="curl -XGET localhost:9200"
# until [safeRunCommand "$command" -eq 0]; do
#     echo "Elastic search still starting..."
#     sleep 1
# done

# eval 

# wait-for-postgres.sh

set -e

host="$1"
shift
cmd="$@"

until curl -XGET "$host":9200; do
  >&2 echo "Elastic is still setting up..."
  sleep 1
done

echo "Elastic has completed setup, executing command."
exec $cmd
#!/usr/bin/env bash
set -euo pipefail

SELF=$(readlink -f "${BASH_SOURCE[0]}")
cd -- "${SELF%%/*/*}"

# ------------------- Create, activate and configure venv -------------------- #
if [[ ! -d ./venv ]]
then
  python3 -m venv venv
fi
source ./venv/bin/activate
pip install -U pip
pip install -U .

# -------------------------------- Functions --------------------------------- #
function append_cmd_help()
{
  local path=$1
  local subcmd=${2:-}
  local cmd
  if [[ -n $subcmd ]]
  then
    cmd=(chemfeat "$subcmd" --help)
    cat >> "$path" << MD

## ${subcmd^}
MD
  else
    cmd=(chemfeat --help)
  fi
  cat >> "$path" << MD

~~~
\$ ${cmd[*]}
$("${cmd[@]}" 2>&1)
~~~
MD
}

function gen_cmd_help()
{
  local path=$1
  cat > "$path" << MD
# Command-Line Usage

The package provides the \`chemfeat\` executable which recognizes several subcommands:
MD
  append_cmd_help "$path"
  for subcmd in calculate configure describe
  do
    append_cmd_help "$path" "$subcmd"
  done
}

function gen_conf()
{
  path=$1
  cat > "$path" << 'CONF'
# Feature-set Configuration File

~~~yaml
CONF
  chemfeat conf >> "$path"
  echo '~~~' >> "$path"
}

# --------------------------------- Generate --------------------------------- #
gen_cmd_help ./doc/source/gen_command_help.md
chemfeat desc -o ./doc/source/gen_features.md
gen_conf ./doc/source/gen_feature_set_configuration.md

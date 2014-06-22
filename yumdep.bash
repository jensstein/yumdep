# bash completion

# inspired by yum.bash from the yum source
# argument: 1 = current word to be completed
_yum_list()
{
    [[ $1 == "" ]] && return

    COMPREPLY+=($(yum -d 0 -C list all "$1*" 2>/dev/null | \
        sed -ne '1d' -e 's/[[:space:]].*//p'))
}

_yumdep()
{
    local cur
    COMPREPLY=()
    cur=$2
    _yum_list "$cur"
}

complete -F _yumdep -o filenames yumdep.py

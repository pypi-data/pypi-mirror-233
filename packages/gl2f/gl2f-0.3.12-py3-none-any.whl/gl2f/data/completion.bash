__gl2f_complete_boards(){
  if [[ "$cur" == */* ]]; then
    local realcur=${cur##*/}
    local prefix=${cur%/*}
    case ${prefix} in
      ## REPLACE_PAGES_SECOND
    esac
  else
    ## REPLACE_PAGES_FIRST

    if declare -F _init_completion >/dev/null 2>&1; then
      [[ $COMPREPLY == */ ]] && compopt -o nospace # not work on mac
    fi

  fi
}


_gl2f(){
  local cur prev words cword split
  if declare -F _init_completion >/dev/null 2>&1; then
    _init_completion -n :/ || return
  else
    COMPREPLY=()
    _get_comp_words_by_ref -n :/ cur prev words cword || return
  fi

  case $cword in
    1)
      COMPREPLY=( $(compgen -W 'auth cat dl local ls open search completion config' -- "$cur") )
      ;;
    *)
      case ${words[1]} in
        auth)
          COMPREPLY=( $(compgen -W 'login remove set-token update' -- "$cur") )
          ;;
        local)
          if [[ $cword == 2 ]]; then
            COMPREPLY=( $(compgen -W 'clear-cache dir export import index install ls stat open build serve' -- "$cur") )
          else
            case ${words[2]} in
              import)
                _filedir
                ;;
              esac
          fi
          ;;
        config)
          COMPREPLY=( $(compgen -W 'create edit path view' -- "$cur") )
          ;;
        cat | dl | ls | open | search)
          __gl2f_complete_boards
          ;;
        esac
      ;;
  esac
}

complete -F _gl2f gl2f

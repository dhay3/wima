function list() {
  # shellcheck disable=SC2034
  for i in {1..15}; do
    ipinfo=$(curl -skm5 ipinfo.io)
    # shellcheck disable=SC2046
    ip=$(awk -F '"' '{print($4)}' <<<$(sed -En '/\"ip\"/p' <<<"${ipinfo}"))
    # shellcheck disable=SC2046
    city=$(awk -F '"' '{print($4)}' <<<$(sed -En '/\"city\"/p' <<<"${ipinfo}"))
    # shellcheck disable=SC2046
    country=$(awk -F '"' '{print($4)}' <<<$(sed -En '/\"country\"/p' <<<"${ipinfo}"))
    # shellcheck disable=SC2046
    org=$(awk -F '"' '{print($4)}' <<<$(sed -En '/\"org\"/p' <<<"${ipinfo}"))
    echo ip: "${ip:-"None"}" city: "${city:-"None"}" country: "${country-"None"}" org: "${org:-"None"}"
  done
}

list

---
cards:
  data:
    path: "{{ .Section }}/{{ .Name }}/data.json"
    source: "https://www.city.ichikawa.lg.jp/pub01/hasseijokyo.html"
  display:
    chart: false
    table: false
date: "{{ .Date }}"
title: '{{ replace .Name "-" " " | title }}'
weight: 10
---

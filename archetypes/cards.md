---
cards:
  chart: false
  data: "{{ .Section }}/{{ .Name }}/data.json"
  source: ""
  table: false
date: "{{ .Date }}"
title: '{{ replace .Name "-" " " | title }}'
weight: 10
---

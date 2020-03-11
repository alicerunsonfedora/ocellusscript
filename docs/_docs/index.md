---
title: Language Reference
layout: default
---

# OcellusScript Language Reference

Welcome to the official documentation page for OcellusScript. The following documentation will guide you through the different aspects of the language and how to complete common tasks.

## Table of Contents

{% for doc in site.docs %}
{% if doc.title != "Language Reference" %}
- [{{ doc.title }}]({{ doc.url }})
{% endif %}
{% endfor %}
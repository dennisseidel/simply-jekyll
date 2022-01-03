---
layout: Post
title: By Tags
permalink: /tags/
content-type: eg
---


<br>
<div>
{% assign tags =  site.notes | map: 'tags' | join: ' '  | split: ' ' | uniq %}
{% for tag in tags %}
        <h3 id="{{ tag }}">{{ tag | capitalize }}</h3>
        {%- for note in site.notes -%}
            {%- if note.tags contains tag -%}
                <li style="padding-bottom: 0.6em; list-style: none;"><a href="{{note.url}}">{{ note.title }}</a></li>
            {%- endif -%}
        {%- endfor -%}
    {%- endfor -%}
</div>
<br/>
<br/>



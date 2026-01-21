# Readme for adapting the templates

*Or: what to where when adapting the ReSpec-generated HTML page*

## Table of contents

- [Relevant folder structures and files](#relevant-folder-structures-and-files)
- [Changing text in text sections](#editing-section-text-in-the-html-page)
- [Changing columns of tables](#changing-columns-of-tables)
- [Changing the header content](#changing-the-header-content)
  - [Contributors section](#contributors-section)
  - [Other relevant attributes](#other-relevant-attributes)
- [Updating the references section](#updating-the-references-section)

### Relevant folder structures and files

There are multiple folders and files, not all of them intended to be modified or customised, or they already have been for this project and do not require further modifications. The relevant ones for understanding the overall principle and (modifiable) source files are as follows.

```
implementation/dcat_ap_lu           % the working directory.
├── respec_resources                % source files for the HTML pages.
│   ├── assets                      % images go here. Note: the name overview.png for
│   │                               % the UML diagram needs to be overview.png and located here.
│   ├── img                         % folder with the logo and callout button. If the logo
│   │                               % needs to be replaced, ensure it's also called logo.png.
│   └── templates                   % the location where templates are specified.
│       ├── base.j2                 % this file is *not* supposed to be modified anymore.
│       ├── main.j2                 % make changes here; if a section is not adapted, it will
│       │                           % fetch the default configuration specified in base.j2.
│       └── custom.j2               % for specifying any additional custom sections.
├── respec                          % place where files are written into.
│   ├── index.html                  % the final ReSpec-generated HTML files
│   ├── *.json                      % automatically generated files as part of the pipeline,
│   │                               % which are read in to generate the HTML file. Do *not* modify.
│   ├── assets                      % images go here. Note: the name overview.png for
│   │                               % the UML diagram needs to be overview.png and located here.
│   └── img                         % folder with the logo and callout button. If the logo
│                                   % needs to be replaced, ensure it's also called logo.png.
├── model2owl-config                % contains various configuration file for model2owl
└── metadata.json                   % contains information that populates the header of the
                                    % HTML file and additional references.
```

### Editing Section Text in the HTML Page

Open `respec_resources/templates/main.j2` and find the line with

```
{% block pageContent %}
```

After that, for any section to be modified:

- Edit the text blocks between the xxxx section-specific block tags, indicated with `{% block xxxx %} .... {% endblock %}`. An example is shown in the figure below for the abstract.

  <img src="implementation/dcat_ap_lu/respec_resources/media/image1.png" width="750" alt="Example of abstract block in main.j2">

- HTML tags can be used as usual, including additional subsection headings (starting with `<h2>` level), whilst remaining within the particular `{% block xxxx %} ... {% endblock %}`.

Take note:

- Do **not** change the lines of code that fetches or processes content from the JSON files (and look like, e.g., ) <img src="implementation/dcat_ap_lu/respec_resources/media/image2.png" width="350" alt="Example of Jinja2 code">

- Do **not** change or remove the section tags.

- Changes made to the text in these sections will be reflected in the HTML page only after (re)running the pipeline.

### Changing columns of tables

This is not recommended. If you want to do so nonetheless, go to the table specification

```html
<table class="data-table simple" id="table-mandatory-classes">
```

Then within the `<thead> ... </thead>` tags, add a new `<th> ... </th>` analogous to the other ones, and adjust the width of other ones to make space. Then, in the `<tbody><tr> ... </tr></tbody>` part, add a new `<td> .. </td>` as appropriate.

### Changing the header content

This happens in the metadata.json file. The first set of fields are self explanatory, like versionInfo and publisher URL. A number of fields are irrelevant for the scope (generating HTML and SHACL shapes), but model2owl requires a value, so please leave them in there.

#### Contributors section

The contributors start on line 28, most of which is self-evident as well, but note the contributor's attribute of role, which can be either `"role": "A"` for author or `"role": "E"` for editor. If someone is both an author and an editor, the contributor data needs to be repeated and the role specified, not contributor once with the role attribute twice.

#### Other relevant attributes

Some others that will be relevant when making changes are:

- title on line 114 in metadata.json, which generates the title of the page, and the version number has to be manually updated there;

- URL updates to "Latest published version" and the like: there are publisher, link, prev, and self in metadata.json.

- Changing the "Copyright © 2025" at the end of the header: in base.j2, change the line containing "Copyright © 2025".

### Updating the references section

There is a central ReSpec database of references that avails of the Specref ecosystem at [https://www.specref.org/](https://www.specref.org/). If a reference key used in the text is also in that database, it will fetch the reference from there and insert it in the References section.

References not in that database must be added in the localBiblio section in the metadata.json file.

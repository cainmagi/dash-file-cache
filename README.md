# Dash File Cache

<p align="center">
  <a href="https://github.com/cainmagi/dash-file-cache/releases/latest"><img alt="GitHub release (latest SemVer)" src="https://img.shields.io/github/v/release/cainmagi/dash-file-cache?logo=github&sort=semver&style=flat-square"></a>
  <a href="https://github.com/cainmagi/dash-file-cache/releases"><img alt="GitHub all releases" src="https://img.shields.io/github/downloads/cainmagi/dash-file-cache/total?logo=github&style=flat-square"></a>
  <a href="https://github.com/cainmagi/dash-file-cache/blob/main/LICENSE"><img alt="GitHub" src="https://img.shields.io/github/license/cainmagi/dash-file-cache?style=flat-square&logo=opensourceinitiative&logoColor=white"></a>
  <a href="https://pypi.org/project/dash-file-cache"><img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/dash-file-cache?style=flat-square&logo=pypi&logoColor=white&label=pypi"/></a>
</p>
<p align="center">
  <a href="https://github.com/cainmagi/dash-file-cache/actions/workflows/python-package.yml"><img alt="GitHub Actions (Build)" src="https://img.shields.io/github/actions/workflow/status/cainmagi/dash-file-cache/python-package.yml?style=flat-square&logo=githubactions&logoColor=white&label=build"></a>
  <a href="https://github.com/cainmagi/dash-file-cache/actions/workflows/python-publish.yml"><img alt="GitHub Actions (Release)" src="https://img.shields.io/github/actions/workflow/status/cainmagi/dash-file-cache/python-publish.yml?style=flat-square&logo=githubactions&logoColor=white&label=release"></a>
</p>

Dash File Cache is a Dash extension library.

Utilities for providing convenient methods to serve cached data in Plotly-Dash or Flask.

The data cache enables the following features:

1. Load a server-side file dynamically and send the file to users (the frontend).
2. Support in-memory files (like `io.BytesIO()`) or on-disk files (specified by a path).
3. Support different kinds of cache (single-thread, multi-processing, or file-based).
4. A customized component helping the dashboard trigger a download event from the server side.

## 1. Install

Intall the **latest released version** of this package by using the PyPI source:

``` sh
python -m pip install dash-file-cache
```

Or use the following commands to install **the developing version** from the GitHub Source when you have already installed [Git :hammer:][tool-git]:

```bash
git clone https://github.com/cainmagi/dash-file-cache
cd dash-file-cache
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m pip install .
```

## 2. Usage

The following codes show a minimal example of this package

```python
from typing import Optional

import io

import dash
from dash import html
from dash import Input, Output

from dash_file_cache import ServiceData, CachePlain

app = dash.Dash("demo")
service = ServiceData(CachePlain(1))
service.serve(app)

app.layout = html.Div(
    (
        html.Div(
            html.P(
                (
                    html.Span("Get Image:", style={"paddingRight": "0.5rem"}),
                    html.Button(id="btn", children="Image"),
                )
            )
        ),
        html.Div((html.P("Cache address:"), html.P(id="addr"))),
        html.Div((html.P("Cached Image:"), html.Img(id="cache"))),
    ),
)


@app.callback(
    Output("addr", "children"),
    Input("btn", "n_clicks"),
    prevent_initial_call=True,
)
def click_get_image(
    n_clicks: Optional[int],
):
    if not n_clicks:
        return dash.no_update

    addr = service.register(
        io.StringIO(
            R'<svg height="100" width="100" xmlns="http://www.w3.org/2000/svg">'
            R'<circle r="45" cx="50" cy="50" fill="red" /></svg>'
        ),
        content_type="image/svg+xml",
        mime_type="image/svg+xml",
        one_time_service=True,
    )
    return addr


@app.callback(
    Output("cache", "src"),
    Input("addr", "children"),
    prevent_initial_call=True,
)
def update_cache(addr):
    if not addr:
        return dash.no_update
    return addr


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8080", debug=True)
```

Check http://127.0.0.1:8080 to see the following results:

|           The minimal demo            |
| :-----------------------------------: |
| ![pic-demo-minimal][pic-demo-minimal] |

## 3. Documentation

Check the documentation to find more details about the examples and APIs.

https://cainmagi.github.io/dash-file-cache/

## 4. Contributing

See [CONTRIBUTING.md :book:][link-contributing]

## 5. Changelog

See [Changelog.md :book:][link-changelog]

[tool-git]:https://git-scm.com/downloads
[tool-nodejs]:https://nodejs.org/en/download/package-manager
[tool-yarn]:https://yarnpkg.com/getting-started/install

[pic-demo-minimal]:https://raw.githubusercontent.com/cainmagi/dash-file-cache/main/display/demo-minimal.png

[link-contributing]:https://github.com/cainmagi/dash-file-cache/blob/main/CONTRIBUTING.md
[link-changelog]:https://github.com/cainmagi/dash-file-cache/blob/main/Changelog.md

# Embedding the Rerun Viewer in a Webpage

<picture>
 <img src="media/webpage_example.gif" alt="">
</picture>

## Used Rerun types

[`Points3D`](https://rerun.io/docs/reference/types/archetypes/points3d), [`LineStrips3D`](https://rerun.io/docs/reference/types/archetypes/line_strips3d), [`Transform3D`](https://www.rerun.io/docs/reference/types/archetypes/transform3d)

## Overview

Static screenshots and videos belong in the past. In this guide, we will walk through deploying a live, interactive webpage integrated with Rerun. By embedding a hosted Rerun viewer, you are not just showing your results — you are handing your audience the keys to explore your data in 3D, scrub through timelines, and inspect your model's logic in real-time.

In a fast-moving industry, the ability to provide an immersive, 'hands-on' demo is the difference between a project that gets glanced at and one that gets remembered. Here we will go through the steps to create your webpage with Rerun integrated, you will see that it is simple and quick process that does not take away valuable development or writing time.

You can see the [resulting webpage here](https://rerun-io.github.io/webpage_example/).

## Useful resources

* [Embed Rerun in Web pages](https://rerun.io/docs/howto/integrations/embed-web)
* API reference:
  * [Web viewer](https://ref.rerun.io/docs/js/stable/web-viewer/index.html)
  * [React web viewer](https://ref.rerun.io/docs/js/stable/web-viewer-react/index.html)
* Rerun web-viewer examples:
  * [Basic](https://github.com/rerun-io/web-viewer-example)
  * [React](https://github.com/rerun-io/web-viewer-react-example)
  * [Svelte](https://github.com/rerun-io/web-viewer-svelte-example)
  * [Serve](https://github.com/rerun-io/web-viewer-serve-example)
  * [Gradio](https://github.com/rerun-io/gradio-rerun-viewer)

---

## How-to guide

This guide goes from nothing to a complete live webpage hosted via [GitHub Pages](https://docs.github.com/en/pages). We assume you are running all commands within the `webpage_example` repository folder and using the [Pixi](https://pixi.sh/latest/#installation) package manager for environment setup (only needed if you want to generate the recordings dataset yourself). To build and host the webpage locally, we make use of [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm).

### 1. Preparing the data (`.rrd` and `.rbl` files)

The first thing you need is data. Record your streams (point clouds, images, transforms) and save them as an `.rrd` file. For this example, we will use the [getting started guide](https://rerun.io/docs/getting-started/data-in/python) to produce our data. The code is prepared in `webpage_example/create_dataset.py`. To save the data to a file instead of logging it to the Rerun viewer, call [`rerun.save`](https://ref.rerun.io/docs/python/stable/common/initialization_functions/#rerun.save) before logging any data. You can also [use `Save recording...` from the file menu](https://rerun.io/docs/getting-started/data-out/export-dataframe#load-the-recording) to export the `.rrd` file directly from the viewer.

Next, set up the blueprint to configure what the viewer displays when the page is opened. The blueprint can be embedded directly in the `.rrd` file, but keeping it separate as an `.rbl` file means you can update the layout without regenerating the recording. This is especially useful if your data is large and slow to produce — the `.rbl` file is typically much smaller and faster to update and upload.

To create the `.rbl` file, comment out `rerun.save` in `webpage_example/create_dataset.py` and call `rr.spawn()` instead. This opens the viewer with the logged data. Arrange the view to your liking, then [use `Save blueprint...` from the file menu](https://rerun.io/docs/concepts/visualization/blueprints#2-save-and-load-files).

> For web deployment, keeping file sizes small is important for fast loading. Prune your data and include only what is necessary for a seamless experience.

### 2. Hosting the data

The webpage fetches the data from a URL. You can host the data wherever you prefer. If the files are small enough, storing them directly in the repository is the simplest option. For larger files, consider a cloud storage service such as Google Drive or OneDrive.

In this example, `dna_structure.rrd` and `dna_structure.rbl` are hosted in the `recordings` folder of this repository.

### 3. Create your webpage

GitHub has thorough documentation for [GitHub Pages](https://docs.github.com/en/pages). The steps below describe the approach taken in this example.

#### Create a GitHub repository

Create a GitHub repository with at least a `README.md` file.

<picture>
  <source media="(prefers-color-scheme: light)" srcset="media/light/create_repo.png">
  <source media="(prefers-color-scheme: dark)" srcset="media/dark/create_repo.png">
  <img alt="Shows the GitHub 'Create a new repository' page." src="media/light/create_repo.png">
</picture>

#### Enable GitHub Pages

In your repository, go to `Settings` → `Pages`. Under `Build and deployment`, set the `Source` to `GitHub Actions`.

<picture>
  <source media="(prefers-color-scheme: light)" srcset="media/light/enable_gh_pages.png">
  <source media="(prefers-color-scheme: dark)" srcset="media/dark/enable_gh_pages.png">
  <img alt="Shows the page to enable 'GitHub Pages' for a repository." src="media/light/enable_gh_pages.png">
</picture>

#### Create a GitHub Actions workflow

Create a file at `.github/workflows/deploy.yml` in your repository (you may need to create the folders). Use the following contents:

```yml
# Simple workflow for deploying static content to GitHub Pages
name: Deploy app to GitHub Pages

on:
  # Runs on pushes targeting the default branch
  push:
    branches: ["main"]

  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:

# Sets the GITHUB_TOKEN permissions to allow deployment to GitHub Pages
permissions:
  contents: read
  pages: write
  id-token: write

# Allow one concurrent deployment
concurrency:
  group: "pages"
  cancel-in-progress: true

jobs:
  # Single deploy job since we're just deploying
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    defaults:
      run:
        # The webpage is defined in the docs folder,
        # so we set it as the default
        working-directory: docs
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install dependencies
        run: npm install

      - name: Build
        run: npm run build
        env:
          REPOSITORY: ${{ github.event.repository.name }}

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          # The folder the action should upload to GitHub Pages.
          # In this example, we are uploading the dist folder inside docs,
          # which is where our static site is built.
          path: "./docs/dist"

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

This workflow assumes the webpage is located in a `docs` folder at the root of the repository, on the `main` branch. Update the paths and branch name as needed. The workflow runs on every push to `main`.

#### Copy the docs folder

Everything related to the webpage in this repository (except for the workflow) is in the `docs` folder. Copy it to your repository to get started.

#### Customize the webpage

The following four files are the main ones you will want to edit:

* `docs/index.html` — the content of your webpage
* `docs/style.css` — the visual style; the supplied stylesheet supports both light and dark themes, switching automatically based on the browser or system setting
* `docs/src/main.ts` — where the interactive Rerun viewer is initialized; update the `rrd` and `rbl` variables to point to your own files
* `docs/package.json` — ensure the `@rerun-io/web-viewer` version here matches the version of the Rerun SDK used to generate the `.rrd` and `.rbl` files

You will also likely want to add your own assets (images, videos, icons) to `docs/assets` and reference them from `docs/index.html`. As well as putting your own `favicon` in the `docs/public` folder.

The remaining files in `docs` can generally be left as-is unless you need more advanced customization.

#### Wait for deployment

After pushing your code, wait for the GitHub Actions workflow to finish. You can monitor its progress in the repository's **Actions** tab.

#### Access your site

Once deployed, your site will be available at `https://your-username.github.io/your-repo-name`, where `your-username` is your GitHub username and `your-repo-name` is your repository name.

## Test your page locally

To test locally, clone the repo and run:

```sh
cd docs
npm install
npm run dev
```

Then open the URL printed to the terminal.

Alternatively, if you are using Pixi, a task is provided:

```sh
pixi run host_webpage
```

## Things to look out for

1. Keep the data files (`.rrd` and `.rbl`) at the same version as `@rerun-io/web-viewer` in `docs/package.json`. In this example, that means the `rerun-sdk` version in `pyproject.toml` (used to generate the data) must match the `@rerun-io/web-viewer` version in `docs/package.json` (used to display the data).

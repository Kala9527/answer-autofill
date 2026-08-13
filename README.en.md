# Answer Autofill

[中文说明](./README.cn.md)

> Local LLM-powered Excel questionnaire answer auto-completion tool with batch processing, dry-run scanning, and safe output files.  

This repository is packaged to be easy to **star, fork, run, remix, and contribute to**. It keeps a dedicated English version for global GitHub discovery, with a separate Chinese version linked above.

## Why Star This

- Practical project idea with a clear real-world use case.
- Small enough to fork, study, and customize quickly.
- English-first bilingual README for both global and Chinese-speaking developers.
- Clean setup instructions, project structure, roadmap, and contribution entry points.
- Built around popular GitHub themes such as AI tools, TypeScript, developer tools, local-first apps, automation, and indie-friendly workflows when relevant.

## What It Does

Local LLM-powered Excel questionnaire answer auto-completion tool with batch processing, dry-run scanning, and safe output files.

## Highlights

- Batch scans .xlsx and .xlsm files
- Writes to output copies instead of changing source spreadsheets
- Uses surrounding survey context to generate better answers
- Dry-run and smoke-test modes for safer batch jobs
- Configurable OpenAI-compatible local model endpoint

## Tech Stack

`	ext
Python, openpyxl, OpenAI SDK, asyncio, httpx
`

## Quick Start

`ash
python -m venv .venv`n.venv\\Scripts\\activate`npip install -r requirements.txt`npython -m answer_autofill "D:\\path\\to\\excel_folder" --dry-run
`

## Project Structure

`	ext
.
|-- src/ or app/          Main source code
|-- public/ or assets/    Static assets when available
|-- docs/                 Notes, specs, or deployment docs when available
|-- README.md             English-first bilingual project guide
-- package / project files
`

## Deployment / Packaging

- Do not commit generated builds, local databases, API keys, private logs, or large media files.
- For frontend projects, deploy the production dist/ folder to GitHub Pages, Vercel, Netlify, Nginx, or package it with DistDesktopLauncher.
- For desktop/mobile projects, publish only release artifacts from a clean build environment.
- Keep configuration examples public and real credentials private.

## Roadmap

- [ ] More spreadsheet layout presets
- [ ] GUI wrapper for non-technical users
- [ ] Result review and approval mode
- [ ] Provider presets and benchmark examples

## Contributing

Issues and pull requests are welcome. Useful contributions include better screenshots, demos, docs, templates, presets, provider guides, compatibility fixes, tests, and translations.

If this project helps you, a star and fork make it easier for more people to discover it.





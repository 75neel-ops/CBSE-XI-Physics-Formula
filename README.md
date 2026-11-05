# Physics Quest by NilanjanC

A responsive, installable static website for CBSE Class XI NCERT Physics revision. It has chapter keywords, Easy / Hard / Extra Hard multiple-choice questions with hints and explanations, a local study-notes question finder, and a year/chapter archive for source-verified school exam questions.

## Publish with GitHub Pages

This site is in `physics-github-pages/`. The workflow in `.github/workflows/pages.yml` publishes that folder whenever changes reach `main`.

1. In the repository, open **Settings → Pages**.
2. Under **Build and deployment**, choose **GitHub Actions** as the source if it is not already selected.
3. The first deployment runs from the Actions tab. The site address will be `https://75neel-ops.github.io/CBSE-XI-Physics-Formula/`.

## Install on devices

Open the Pages URL over HTTPS. On Android Chrome use **⋮ → Install app** or **Add to Home screen**. On iPhone/iPad Safari use **Share → Add to Home Screen**. On desktop Chrome or Edge use the install icon or browser menu. The app shell and study guide are cached after the first visit; Gemini-based answers are not part of this static deployment.

## Gemini and privacy

GitHub Pages serves public HTML, CSS and JavaScript. It cannot read a private Streamlit secret at runtime. Never put an API key in the browser code or commit it to this repository. The Ask section searches the local chapter notes. A private server or serverless function is needed to call Gemini securely for all students.

## Exam questions

The archive starts empty because Class XI finals are set by schools and there is no single common CBSE Class XI final paper. Importing a CSV is available for local review in that browser. For a permanent shared archive, commit source-verified rows in a data file and update the site renderer; include each paper's attribution/source link.

The chapter list follows the [CBSE Class XI Physics curriculum 2026–27](https://cbseacademic.nic.in/web_material/CurriculumMain27/SecPart2/Physics_SecP2_2026-27.pdf). Refer to the [NCERT textbook portal](https://ncert.nic.in/textbook.php?keph1=0-14) for the current textbook.


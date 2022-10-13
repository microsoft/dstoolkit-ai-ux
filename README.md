# Project

Welcome to the AI Gallery. This repo hosts multiple demos for AI use-cases across multiple industries. The purpose of this repository is to collect, share, and improve demos developped for AI products/solutions/services which have been proven impactful.

## 🚀 Adding your demo to the gallery

Currently, the onboarding process of new demos handles demos that are self hosted in your own project subscription. In other words, if your demo can be accessed via an URL, you can follow the steps below. If you need to host your demos in Azure, you may contact one of the contributor and we will help you onboard it.

This repository is fully config driven, making it easy to add your own demo in here.

To add your UI demo, the steps you need to take are:

1. Create your own branch: "your-name"/"your-demo"
2. Add a thumbnail of your UI (600 pixels x 400 pixels) to `gallery/app/static/assets/img/demo_thumbnails`
3. Add a screenshot of your UI (1600 pixels x 900 pixels) to `gallery/app/static/assets/img/demo_screenshots`
4. Add a new yaml file to `gallery/app/demo_configs`, following the yaml structure of the other demo configs as described below
5. Add the name of the `yml` file to the `gallery/app/demo_configs/.order` file in the position you'd like it to appear
6. Create a pull request from your branch to "develop" branch. Once accepted, you will be able to view your demo here: https://dstoolkit-gallery-dev.com/gallery.
7. If your demos is working correctly and all the information is correct, create a new pull request from "develop" to "main" to push the demo to the main page.

### yml file structure

| yml key         | Description of Value                                                                                    |
| --------------- | ------------------------------------------------------------------------------------------------------- |
| name            | Descriptive name of your demo                                                                           |
| tagline         | Short tagline to be shown on the gallery front page                                                     |
| industry        | The specific main industry (e.g. "Energy", "Retail") or "Cross-Industry"                                |
| use_case_type   | The data science use case of your demo                                                                  |
| license         | The licence of the code associated with this demo                                                       |
| main_technology | The main technology(ies) used in this demo e.g. "Flask", "Streamlit", "Django", "node.js"               |
| released        | The date this demo was released                                                                         |
| updated         | The date this demo was last updated (optional)                                                          |
| authors         | key-values of the authors' names and github alias                                                       |
| description     | A description of your demo                                                                              |
| feature_bullets | Bullets that describe in brief the feature components of your demo and the technologies that drive them |
| images          | Filenames of the screenshot and thumbnail for your demo to be shown in the gallery                      |
| links           | Links to the demo, source code and [optionally] download link for the code                              |

### Valid Industries

You may assign only **one** of the valid use case types to your demo:

- Cross-Industry
- Agriculture
- Automotive
- Banking
- Defense
- Energy
- Healthcare
- Insurance
- Life Sciences
- Manufacturing
- Media
- Mining
- Public Sector
- Retail
- Telecomms
- Travel

### Valid Use Case Types

You may assign only **one** of the valid use case types to your demo:

- Classification
- Clustering
- NLP
- Optimization
- Regression
- Search
- Vision
- Other

## 🔔 (Coming Soon)

- We are working on the infrastructure to enable you to host your demo on our subscription (MSFT employees only for now). With this feature, you will only have to provide your app folder and a docker image.

## Contributing

This project welcomes contributions and suggestions. Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.

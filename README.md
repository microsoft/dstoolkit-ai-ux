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

| yml key                 | Description of Value                                                                           |
|-------------------------|------------------------------------------------------------------------------------------------|
| name                    | Descriptive name of your demo                                                                  |
| tagline                 | Short tagline to be shown on the gallery front page                                            |
| authors                 | Update yml file structure doc                                                                  |
| business_problem        | The business problem that your accelerator seeks to solve as a string or list of bullet points |
| business_value          | The value provided to the business in using this accelerator                                   |
| accelerator_description | A description of your accelerator and how it solves the business problem                       |
| value                   | The value provided to the user/data scientist that is using this accelerator                   |
| architecture            | Bulleted list of technologies this accelerator leverages                                       |
| images                  | Filenames of the screenshot and thumbnail for your demo to be shown in the gallery             |
| links                   | Links to the demo, source code and [optionally] ARM template to deploy the solution            |


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

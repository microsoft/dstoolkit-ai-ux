# Front-end page

This folder contains the configuration files for all the demos and the web app for the AI-gallery landing page.

# Adding your demo to the gallery

This application is fully config driven, making it easy to add your own demo in here.

To add your UI demo, the steps you need to take are:
- Create your own branch: "your-name"/"your-demo"
- Add a thumbnail of your UI (600 pixels x 400 pixels) to `static/assets/img/demo_thumbnails`
- Add a screenshot of your UI (1600 pixels x 900 pixels) to `static/assets/img/demo_screenshots`
- Add a new yaml file to `demo_configs`, following the yaml structure of the other demo configs as described below
- Add the name of the `yml` file to the `demo_configs/.order` file in the position you'd like it to appear
- Create a pull request

## yml file structure

| yml key                 | Description of Value                                                                           |
|-------------------------|------------------------------------------------------------------------------------------------|
| name                    | Descriptive name of your demo                                                                  |
| tagline                 | Short tagline to be shown on the gallery front page                                            |
| authors                 | The specific main industry (e.g. "Energy", "Retail") or "Cross-Industry"                       |
| business_problem        | The business problem that your accelerator seeks to solve as a string or list of bullet points |
| business_value          | The value provided to the business in using this accelerator                                   |
| accelerator_description | A description of your accelerator and how it solves the business problem                       |
| value                   | The value provided to the user/data scientist that is using this accelerator                   |
| architecture            | Bulleted list of technologies this accelerator leverages                                       |
| images                  | Filenames of the screenshot and thumbnail for your demo to be shown in the gallery             |
| links                   | Links to the demo, source code and [optionally] ARM template to deploy the solution            |



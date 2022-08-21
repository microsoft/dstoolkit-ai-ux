
# Adding your demo to the gallery

This application is fully config driven, making it easy to add your own demo in here.

To add your UI demo, the steps you need to take are:
- Create your own branch: "your-name"/"your-demo"
- Add a thumbnail of your UI (600 pixels x 400 pixels) to `static/assets/img/demo_thumbnails`
- Add a screenshot of your UI (1600 pixels x 900 pixels) to `static/assets/img/demo_screenshots`
- Add a new yaml file to `demo_configs`, following the yaml structure of the other demo configs
- Add the name of the `yml` file to the `demo_configs/.order` file in the position you'd like it to appear
- Create a pull request

## yml file structure

| yml key         | Description of Value                                                                                    |
|-----------------|---------------------------------------------------------------------------------------------------------|
| name            | Descriptive name of your demo                                                                           |
| tagline         | Short tagline to be shown on the gallery front page                                                     |
| industry        | The specific main industry (e.g. "Energy", "Retail") or "Cross-Industry"                                |
| use_case_type   | The data science use case of your demo                                                                  |
| license         | The licence of the code associated with this demo                                                       |
| main_technology | The main technology(ies) used in this demo e.g. "Flask", "Streamlit", "Django", "node.js"               |
| released        | The date this demo was released                                                                         |
| updated         | The date this demo was last updated (optional)                                                          |
| authors         | key-values of the authors names and github alias                                                        |
| description     | A description of your demo                                                                              |
| feature_bullets | Bullets that describe in brief the feature components of your demo and the technologies that drive them |
| images          | Filenames of the screenshot and thumbnail for your demo to be shown in the gallery                      |
| links           | Links to the demo, source code and [optionally] download link for the code                              |

### Valid Industries

Your demo can be "Cross-Industry" or it can be one of:
- Agriculture
- Automotive
- Banking
- Defense
- Energy
- Healthcare
- Insurance
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

The valid use case types that you can assign your demo are:
- Classification
- Clustering
- NLP
- Optimization
- Regression
- Search
- Vision
- Other

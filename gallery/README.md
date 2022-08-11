
# Deployment

[![Deploy To Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fmicrosoft%2Fdstoolkit-ai-ux%2Fgallery-dev%2Fgallery%2Fapp%2Fazuredeploy.json)

# Adding your demo link to the gallery 

This application is fully config driven, making it easy to add your own demo in here.

To add your UI demo, the steps you need to take are:
- Create your own branch: <your-name>/<your-demo>
- Add a thumbnail of your UI (600 pixels x 400 pixels) to `static/assets/img/demo_thumbnails`
- Add a screenshot of your UI (1600 pixels x 900 pixels) to `static/assets/img/demo_screenshots`
- Add a new yaml file to `demo_configs`, following the yaml structure of the other demo configs
- Add the name of the `yml` file to the `demo_configs/.order` file in the position you'd like it to appear
- Create a pull request

# [COMING SOON] Hosting your demo in ACR and adding it to the gallery 

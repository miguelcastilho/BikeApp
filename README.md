# BikeApp
With BikeApp users can report stolen bikes. If other users see the stolen bike, they can send a message to the owner to inform them of the location of the bike.

## Deploy to Cloud Foundry
Clone the project:
```sh
$ git clone https://github.com/miguelcastilho/BikeApp.git
$ cd BikeApp
```

To deploy the storage service, first create a MySQL service instance named **mysql** and then push the app:
```sh
$ cf create-service mysql-dev default mysql-dev
$ cd storage_service
$ cf push
```

Deploy the email service:
```sh
$ cd email_service
$ cf push
```

Set the environment variable to be used by GMAIL to sent emails:
```
$ cf set-env email-service GMAIL_USER <gmail_user>
$ cf set-env email-service GMAIL_PASSWORD <gmail_password>
```

Deploy the webui service:
```sh
$ cd webui
$ cf push
```

## Workflow
1. Open http://webui.hcf.euwest1.stackato.net in **Chrome** (sorry, other browsers are not supported);
2. Click on **Report a bike as stolen**, fill in all the details and click **Submit**:
   * Example url for a photo: https://upload.wikimedia.org/wikipedia/commons/4/41/Left_side_of_Flying_Pigeon.jpg
   * Please use a valid email address. This email will be used to receive notifications about sightings of your bike;
   * To select the location please **click&drag** the red balloon.
3. Click **Browse stolen bikes** and scroll down until you find your bicycle;
4. Click **I have seen this bike** and fill in description, set the location and click **Submit**;
5. After a few minutes you should get an email telling you that your bike has been seen.

## Architecture
* webui:
  * Only tested with **Chrome**, might not work on IE or Firefox!
  * Provide the user interface;
  * Mobile friendly;
  * Uses Google Maps to pick the location of stolen or seen bicycles;
  * Uses HavenOnDemand Map Coordinates API to display the country in which a bicycle was stolen;
  * AngularJS application;
  *	Uses the staticfile-buildpack;
* storage-service:
  * Stores records for each stolen bicycle;
  * Python application using Flask;
  * Uses a MySQL service instance as a backend.
* email-service:
  * Sends email to the owner of a bicycle when it was reported as seen;
  * Python application using Flask;
  * Uses Gmail API to send emails;

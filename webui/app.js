var bikeApp = angular.module('bikeApp', ['ngRoute', 'angular-location-picker']);
var emailServiceUrl = "http://email-service.hcf.euwest1.stackato.net";
var storageServiceUrl = "http://storage-service.hcf.euwest1.stackato.net";

bikeApp.config(['$locationProvider', '$routeProvider',
    function config($locationProvider, $routeProvider) {
      $locationProvider.hashPrefix('!');

      $routeProvider.
        when('/bikes', {
          template: '<bike-list></bike-list>'
        }).
        when('/about', {
          templateUrl: 'about/about.template.html'
        }).
        when('/report-stolen', {
          template: '<report-stolen></report-stolen>'
        }).
        when('/thanks-stolen', {
          templateUrl: 'thanks/thanks-stolen.template.html'
        }).
        when('/thanks-seen', {
          templateUrl: 'thanks/thanks-seen.template.html'
        }).
        when('/report-seen/:bikeId', {
          template: '<report-seen></report-seen>'
        }).
        otherwise('/bikes');
    }
  ]);

bikeApp.component('bikeList', {
    templateUrl: 'bike-list/bike-list.template.html',
    controller: function ($scope, $http) {
        $scope.bikes = []

        $http({
          method: 'GET',
          url: storageServiceUrl + "/List",
        }).then(function success(resp) {
          for (index = 0; index < resp.data.length; ++index) {
            d = resp.data[index].Bicycle;

            bike = {
              id: d.bicycle_id,
              description: d.description,
              serial: d.serial_no,
              colour: d.colour,
              // TODO: photo, lat, lon
              lat: 39.90,
              lon: 116.40,
              brand: d.make,
              locked: d.locked,
              photo: null,
              country: null
            };

            $scope.bikes.push(bike);


            (function(frozen_bike) {
              $http({
                method: 'GET',
                url: 'https://api.havenondemand.com/1/api/sync/mapcoordinates/v1?targets=country&lat=' + bike.lat + '&lon=' + bike.lon + '&apikey=5ec0d106-9f58-4019-8078-ea8ea1cc7282'
              }).then(function success(resp) {
                if (resp.data.matches.length > 0) {
                  frozen_bike.country = resp.data.matches[0].name;
                }
              });
            })(bike);

          }
        }, function error(resp) {
          alert("Error sending email: " + resp);
        });
    }
  });

bikeApp.component('reportStolen', {
    templateUrl: 'report-stolen/report-stolen.template.html',
    controller: function ($scope, $location, $http) {

      $scope.location = {latitude: 53.270962, longitude: -9.062691};

      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position){
          $scope.$apply(function(){
            $scope.location = {
              latitude: position.coords.latitude,
              longitude: position.coords.longitude
            }
          });
        });
      }

      $scope.formData = {};
      // Defaults
      $scope.formData.date = null;
      $scope.formData.description = '';
      $scope.formData.contact = "";
      $scope.formData.locked = true;
      $scope.formData.photo = '';
      $scope.formData.serial = '';
      $scope.formData.colour = '';
      $scope.formData.brand = '';
      $scope.formData.longitude = $scope.location.longitude;
      $scope.formData.latitude = $scope.location.latitude;

      $scope.onLocationChange = function(location){
        $scope.formData.longitude = location.longitude;
        $scope.formData.latitude = location.latitude;
      }

      $scope.processForm = function() {
        var data = {
          "brand": $scope.formData.brand,
          "serial_no": $scope.formData.serial,
          "description": $scope.formData.description,
          "colour": $scope.formData.colour,
          "owner_contact": $scope.formData.contact,
          "locked": $scope.formData.locked,
          "date_stolen": $scope.formData.date,
          // TODO: photo, lon, lat
        }

        $http({
          method: 'POST',
          url: storageServiceUrl + "/AddReport",
          data: data,
          headers: {'Content-Type': 'application/json'}
        }).then(function success(resp) {
          console.log("Saved")
        }, function error(resp) {
          alert("Error saving: " + resp);
        });

        $location.path('thanks-stolen');
      };
    }
  });

bikeApp.component('reportSeen', {
  templateUrl: 'report-seen/report-seen.template.html',
  controller: function ($scope, $location, $routeParams, $http) {
    $scope.location = {latitude: 53.270962, longitude: -9.062691};

    $scope.formData = {};
      // Defaults
      $scope.formData.description = '';
      $scope.formData.longitude = $scope.location.longitude;
      $scope.formData.latitude = $scope.location.latitude;

      $scope.onLocationChange = function(location){
        $scope.formData.longitude = location.longitude;
        $scope.formData.latitude = location.latitude;
      }

      $scope.processForm = function() {
        console.log($routeParams.bikeId)

        $http({
          method: 'GET',
          url: storageServiceUrl + "/ViewStolenReport",
          params: {"bicycle_id": $routeParams.bikeId},
          headers: {'Content-Type': 'application/json'}
        }).then(function success(resp) {
          console.log(resp)
        }, function error(resp) {
          alert("Error saving: " + resp);
        });

        // get email via bike id
        var email = "jonas.pfannschmidt@gmail.com"

        var data = {
          "lon": $scope.formData.longitude,
          "lat": $scope.formData.latitude,
          "description": $scope.formData.description,
          "recipient": email
        }

        $http({
          method: 'POST',
          url: emailServiceUrl,
          data: data,
          headers: {'Content-Type': 'application/json'}
        }).then(function success(resp) {
          console.log("Email sent!")
        }, function error(resp) {
          alert("Error sending email: " + resp);
        });

        $location.path('thanks-seen');

      };
    }
});

bikeApp.directive('bsActiveLink', ['$location', function ($location) {
return {
    restrict: 'A', //use as attribute 
    replace: false,
    link: function (scope, elem) {
        //after the route has changed
        scope.$on("$routeChangeSuccess", function () {
            var href = '#!' + $location.path();
            angular.forEach(elem.find('a'), function (a) {
                a = angular.element(a);
                if (href == a.attr('href')) {
                    a.parent().addClass('active');
                } else {
                    a.parent().removeClass('active');   
                };
            });     
        });
    }
}
}]);
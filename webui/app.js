var bikeApp = angular.module('bikeApp', ['ngRoute', 'angular-location-picker']);

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
    controller: function ($scope) {
        $scope.bikes = [
        {
          id: 1,
          description: 'A black pepperbike. I left it in front of the Kingshead. When I came out after a few pints it was gone.',
          serial: '123-abcd',
          colour: 'Black',
          lat: 58.2,
          lon: 13,
          brand: 'Pepperbikes',
          locked: true,
          photo: "http://www.pepperbikes.de/media/catalog/product/cache/1/image/574x359/9df78eab33525d08d6e5fb8d27136e95/t/r/trekkingrad_tp1411st_gb_frontal.jpg"
        }, {
          id: 2,
          description: 'A blue pepperbike. I left it in front of the Crane Bar. When I came out after a few shots it was gone.',
          serial: '456-abcd',
          colour: 'Blue',
          lat: 58.5,
          lon: 13.1,
          brand: 'Pepperbikes',
          locked: false,
          photo: "http://www.pepperbikes.de/media/catalog/product/cache/1/image/574x359/9df78eab33525d08d6e5fb8d27136e95/t/r/trekkingrad_tp1411st_gb_frontal.jpg"
        }, {
          id: 3,
          description: 'A red pepperbike. I left it in front of Roisin Dubh. When I came out after a few glasses it was gone.',
          serial: '789-abcd',
          colour: 'Red',
          lat: 58.4,
          lon: 13.3,
          brand: 'Pepperbikes',
          locked: true,
          photo: null
        }
      ];
    }
  });

bikeApp.component('reportStolen', {
    templateUrl: 'report-stolen/report-stolen.template.html',
    controller: function ($scope, $location) {

      $scope.location = {latitude: 53.270962, longitude: -9.062691};

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
        $location.path('thanks-stolen');

      };
    }
  });

bikeApp.component('reportSeen', {
  templateUrl: 'report-seen/report-seen.template.html',
  controller: function ($scope, $location, $routeParams) {
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
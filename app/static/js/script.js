angular.module('ticketApp', ['ngAnimate', 'ui.bootstrap'])
    .controller('NewTicketController', function($scope) {
      $scope.minDate = new Date();
      $scope.dt = $scope.minDate;
    })
    .controller('ViewTicketController', function($scope) {

    });

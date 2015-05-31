(function(){
  'use strict';
  var module = angular.module('app', ['onsen']);

  module.controller('AppController', function($scope, $data) {
    $scope.doSomething = function() {
      ons.notification.alert({message: 'Hello, World!'});
    };
  });

  module.controller('DetailController', function($scope, $data) {
    $scope.item = $data.selectedItem;
  });

  module.controller('MasterController', function($scope, $data) {
    $scope.items = $data.items;  
    
    $scope.showDetail = function(index) {
      var selectedItem = $data.items[index];
      $data.selectedItem = selectedItem;
      $scope.navi.pushPage('detail.html', {title : selectedItem.title});
    };
  });

  module.factory('$data', function() {
      var data = {};
      
      data.items = [
          { 
              title: 'Ken Robinson',
              label: '1',
              desc: 'Author/educator'
          },
          { 
              title: 'Amy Cuddy',
              label: '2',
              desc: 'Social Psychologist'
          },
          { 
              title: 'Simon Sinek',
              label: '3',
              desc: 'Leadership expert'
          },
          { 
              title: 'Brené Brown',
              label: '4',
              desc: 'Vulnerability researcher'
          }
      ]; 
      
      return data;
  });
})();


bineControllers.controller('bookListControl', 
		['$rootScope', '$scope', '$sce', '$http', 
function ($rootScope, $scope, $sce, $http) {
	
	$scope.load_book_list = function() {
		$http.get('/book/').success(function(data) {
			$scope.books = data;
		});
	}
			
	$scope.load_book_list();
}]);
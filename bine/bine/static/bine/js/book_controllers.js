bineControllers.controller('bookListControl', [ '$rootScope', '$scope', '$sce',
		'$http', function($rootScope, $scope, $sce, $http) {

			$rootScope.note = null;
			$scope.user = $rootScope.user;
			if (!$scope.user)
				location.href = "#/login/";

			$scope.load_book_list = function() {
				$http.get('/book/').success(function(data) {
					$scope.books = data;
				});
			}

			$scope.load_book_list();
		} ]);
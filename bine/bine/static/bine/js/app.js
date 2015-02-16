var bineApp = angular.module('bineApp', [ 'ngRoute', 'ngCookies', 'ngSanitize',
		'angular-jwt', 'angularFileUpload' ]);

bineApp.config([ '$routeProvider', function($routeProvider) {
	$routeProvider.when('/login/', {
		templateUrl : '/static/bine/html/login.html',
		controller : 'UserAuthControl'
	}).when('/register/', {
		templateUrl : '/static/bine/html/register.html',
		controller : 'UserAuthControl'
	}).when('/note/', {
		templateUrl : '/static/bine/html/note_list.html',
		controller : 'NoteListControl'
	}).when('/note/new/', {
		templateUrl : '/static/bine/html/note_form.html',
		controller : 'NoteNewControl'
	}).when('/note/:note_id/', {
		templateUrl : '/static/bine/html/note_detail.html',
		controller : 'NoteDetailControl'
	}).when('/book/', {
		templateUrl : '/static/bine/html/book_list.html',
		controller : 'bookListControl'
	}).otherwise({
		redirectTo : '/login/'
	});
} ]);

bineApp.service('userService', [ '$http', '$window', 'jwtHelper',
		function($http, $window, jwtHelper) {
			this.user = null;
			this.token = null;

			this.clear = function() {
				this.user = null;
				this.token = null;
			}

			this.check_auth_and_set_user = function($scope) {
				var token = this.get_token();
				if (token && !jwtHelper.isTokenExpired(token)) {
					$scope.user = this.user;
					return true;
				} else {
					location.href = "#/login/";
					return false;
				}
			}

			this.set_token_and_user_info = function(data) {
				this.set_token(data.token);
				this.user = data.user;
			}

			this.set_token = function(token) {
				// $window.sessionStorage.token = token;
				this.token = token;
			}

			this.get_token = function() {
				// return $window.sessionStorage.getItem('token');
				return this.token;
			}
		} ]);

bineApp.config(function Config($httpProvider, jwtInterceptorProvider) {
	jwtInterceptorProvider.authPrefix = 'JWT ';
	jwtInterceptorProvider.tokenGetter = [ 'userService',
			function(userService) {
				return userService.get_token();
			} ];

	$httpProvider.interceptors.push('jwtInterceptor');
})

/*
 * bineApp.factory('AuthInterceptor', function(userService, $q) { return {
 * request : function(config) { config.headers = config.headers || {};
 * 
 * var token = userService.get_token(); if (token) {
 * config.headers.Authorization = 'Bearer ' + token; } return config ||
 * $q.when(config); }, response : function(response) { if (response.status ===
 * 401) { locaiton.href = "#/login/" } return response || $q.when(response); } };
 * });
 *  // Register the previously created AuthInterceptor.
 * bineApp.config(function($httpProvider) {
 * $httpProvider.interceptors.push('AuthInterceptor'); });
 */

bineApp.filter('truncate', function() {
	return function(content, maxCharacters) {
		if (content == null)
			return "";

		content = "" + content;
		content = content.trim();
		if (content.length <= maxCharacters)
			return content;

		content = content.substring(0, maxCharacters);
		var lastSpace = content.lastIndexOf(" ");
		if (lastSpace > -1)
			content = content.substr(0, lastSpace);

		return content + '...';
	};
});

var bineApp = angular.module('bineApp', [
                             'ngRoute',
                             'ngSanitize',
                             'angularFileUpload',
                             'bineControllers'
                             ]);

bineApp.config(['$routeProvider',
                function($routeProvider) {
                  $routeProvider.
                    when('/note/', {
                      templateUrl: '/static/bine/html/note_list.html',
                      controller: 'NoteListControl'
                    }).
                    when('/note/new/', {
                        templateUrl: '/static/bine/html/note_form.html',
                        controller: 'NoteNewControl'
                      }).
                      
                    when('/note/:note_id/', {
                      templateUrl: '/static/bine/html/note_detail.html',
                      controller: 'NoteDetailControl'
                    }).
                    otherwise({
                      redirectTo: '/note/'
                    });
                }]);

bineApp.config(['$httpProvider', function($httpProvider) {
	    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
	    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	}
]);

bineApp.filter('truncate', function () {
    return function (content, maxCharacters) {
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


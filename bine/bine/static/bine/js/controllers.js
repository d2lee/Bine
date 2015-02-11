var bineControllers = angular.module('bineControllers', []);

bineControllers.controller('NoteListControl', ['$scope', '$sce', '$http',
  function ($scope, $sce, $http) {
		$http.get('/note/').success(function(data) {
		$scope.notes = data;
		
		$scope.convertPreferenceToHtml = function (preference) {
			var spanHtml = "";
			
			for (i = 0; i < preference; i++ ) {
				spanHtml = spanHtml + "<span class='glyphicon glyphicon-star'></span>";
			}
			
			return $sce.trustAsHtml(spanHtml);
		}
    });
  }]);

bineControllers.controller('NoteDetailControl', ['$scope', '$routeParams', '$http', 
  function ($scope, $routeParams, $http) {
	var note_id = $routeParams.note_id;
	
	$scope.note_id = note_id;
	$scope.new_reply_content = "";
	$scope.current_reply = "";
	
	// fetch the details about current booknote.
	var note_target_url = '/note/' + note_id + "/";
	$http.get(note_target_url).success(function(data) {
		$scope.note = data;
	});
	
	// fetch the reply information from server.
	var note_reply_url = '/note/' + note_id + "/reply/";
	$http.get(note_reply_url).success(function(data) {
		$scope.replies = data;
	});
	
	$scope.delete_reply = function (reply, index) {
		var url = url = '/note/' + $scope.note_id + '/reply/' + reply.id + "/";
		
		$http.delete(url).
		  success(function(data, status, headers, config) {
			  $scope.replies.splice(index,1)
		  }).
		  error(function(data, status, headers, config) {
		      alert("error");
		  });
	}
	
	$scope.update_reply = function (reply) {
		$scope.current_reply = reply;
		$scope.new_reply_content = reply.content;
		$('#reply_modal').modal('show');
	};
	
	$scope.save_reply = function () {
		if ($scope.new_reply_content != $scope.current_reply.content) {
			$scope.current_reply.content = $scope.new_reply_content;
		}
		
		var data = {};
		var url = "";
		
		if ($scope.current_reply == '') { // create
			data = {
					'user': 2,
					'content': $scope.new_reply_content
					};
			url = '/note/' + $scope.note_id + '/reply/';
		}
		else { // update
			data = {
					'content': $scope.new_reply_content
					};
			url = '/note/' + $scope.note_id + '/reply/' + $scope.current_reply.id + "/";
		}
		
		
		$http.post(url, data).
		  success(function(data, status, headers, config) {
			  if ($scope.current_reply == '') {
				$scope.replies.push(data);  
			  }
			  
			  $('#reply_modal').modal('hide');
		  }).
		  error(function(data, status, headers, config) {
		      alert("error");
		  });
	}
	
	$scope.create_reply = function (reply) {
		$scope.new_reply_content = '';
		$scope.current_reply = '';
		$('#reply_modal').modal('show');
	}
}]);

bineControllers.controller('NoteNewControl', ['$scope', '$sce', '$http',
    function ($scope, $sce, $http) {
	}
]);
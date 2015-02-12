var bineControllers = angular.module('bineControllers', []);

bineControllers.controller('NoteListControl', ['$rootScope', '$scope', '$sce', '$http',
  function ($rootScope, $scope, $sce, $http) {
		$rootScope.note = null;
	
		$http.get('/note/').success(function(data) {
		$scope.notes = data;
		
		$scope.convertPreferenceToHtml = function (preference) {
			var spanHtml = "";
			
			for (i = 0; i < preference; i++ ) {
				spanHtml = spanHtml + "<span class='glyphicon glyphicon-star'></span>";
			}
			
			return $sce.trustAsHtml(spanHtml);
		}
		
		$scope.edit_note = function (note) {
			$rootScope.note = note;
			location.href = "#/note/new/"
		}
		
		$scope.delete_note = function (note, index) {
			var url = "/note/" + note.id + "/";
			$http.delete(url).success(function(data){
				alert('삭제되었습니다.');
				$scope.notes.splice(index,1);
			});
		}
		
		$scope.update_likeit = function (note) {
			var url = "/note/" + note.id + "/likeit/";
			$http.post(url).success(function(data) {
				note.likeit = data.likeit;
			});
		}
		
		$scope.convertShareToHtml = function(share_to) {
			var text = "";
			switch (share_to) {
			case 'P': 
				text = "개인";
				break;
			case 'F':
				text = "친구";
				break;
			case 'A':
				text = "모두";
				break;
			}
			return text;
		}
		
		$scope.showAttachHtml = function(attach_url) {
			var html = "";
			if (attach_url) {
				html = "<a href='" + attach_url + "'>첨부파일(1)</a>";
			}
			return $sce.trustAsHtml(html);
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
	
	$scope.convertShareToHtml = function(share_to) {
		var text = "";
		switch (share_to) {
		case 'P': 
			text = "개인";
			break;
		case 'F':
			text = "친구";
			break;
		case 'A':
			text = "모두";
			break;
		}
		return text;
	}
}]);

bineControllers.controller('NoteNewControl', ['$rootScope', '$scope', '$sce', '$upload', '$http', 
    function ($rootScope, $scope, $sce, $upload, $http) {
		
		if ($rootScope.note == null) {
			var today = new Date();
			
			$scope.note = {
					'user': {'id':2},
					'preference': 3, 
					'share_to': 'F',
					'read_date_from': today,
					'read_date_to': today,
			};
			$scope.book_title = "";
		}
		else {
			$scope.note = $rootScope.note;
			$scope.book_title = $scope.note.book.title;
			
			// convert string date to date object to initialize input date object.
			$scope.note.read_date_from = new Date($scope.note.read_date_from);
			$scope.note.read_date_to = new Date($scope.note.read_date_to);
		}
		
		$scope.save = function() {
			var note = $scope.note;
			var id = null;
			
			if (note.id != null)
				id = note.id;
				
			var data = {
					'id': id,
					'user': note.user.id,
					'book': note.book.id,
					'content': note.content,
					'read_date_from': $scope.format_date(note.read_date_from),
					'read_date_to': $scope.format_date(note.read_date_to),
					'preference': note.preference,
					'share_to': note.share_to,
					'attach': note.attach, 
			};
			
			var url = '/note/';
				
			if ($scope.note.id != null) { // update
				url = url + $scope.note.id + "/";
			}
			
			$scope.upload(url, data, $scope.note.attach)
			/*
			var attach = $scope.note.attach;
			if (attach) {
				$scope.upload(url, attach, data);
			}
			else {
				$http.post(url, data).
				  success(function(data, status, headers, config) {
					  alert('성공적으로 저장되었습니다.');
					  
				  }).
				  error(function(data, status, headers, config) {
				      alert("error");
				  });
			}
			*/
		}
		
		$scope.set_preference = function(pref) {			
			for (var i = 1; i <= 5; i ++) {
				if (i <= pref)
					$('#pref-' + i).css('color', '#337ab7');
				else
					$('#pref-' + i).css('color', '#333');
			}
			
			$scope.note.preference = pref;
		}
		
		$scope.set_preference($scope.note.preference);
		
		$scope.search_book = function() {
			var title = $scope.book_title;
			
			if (title == '') {
				alert('검색할 책 이름을 입력하십시오.')
				return;
			}
			else {
				var url = "/book/?title=" + $scope.book_title;
				
				$http.get(url).
				  success(function(data, status, headers, config) {
					  $scope.books = data;
					  $('#book_search_modal').modal('show');
				  }).
				  error(function(data, status, headers, config) {
				      alert("error");
				  });
			}
		}
		
		$scope.select_book = function(book) {
			$scope.note.book = book;
			$scope.book_title = book.title;
			$('#book_search_modal').modal('hide');
		}
		
		$scope.format_date = function(date) {
			var year = date.getFullYear();
			var month = (1 + date.getMonth()).toString();
			month = month.length > 1 ? month : '0' + month;
			var day = date.getDate().toString();
			day = day.length > 1 ? day : '0' + day;
			return year + '-' + month + '-' + day;
		}
		
		$scope.upload = function (url, data, file) {
	        $upload.upload({
                    url: url,
                    method: 'POST',
                    fields: data,
                    fileFormDataName: 'attach',
                    file: file
                }).progress(function (evt) {
                    var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
                    //console.log('progress: ' + progressPercentage + '% ' + evt.config.file.name);
                }).success(function (data, status, headers, config) {
                	alert('성공적으로 저장되었습니다.');
                    //console.log('file ' + config.file.name + 'uploaded. Response: ' + data);
                });
	    };
	}
]);
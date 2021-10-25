$("#saveProfileBtn").click(function (e) {
    e.preventDefault();
    var categories = $('#category-picker').val();
    console.log(categories);
    $.ajax({
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name=csrfmiddlewaretoken]').val())
        },
        type: 'PUT',
        url: '/news/profile/update/',
        data: {
            "categories": JSON.stringify(categories)
        }
    })
});

$("#removePictureBtn").click(function (e) {
    e.preventDefault();
    $.ajax({
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name=csrfmiddlewaretoken]').val())
        },
        type: 'DELETE',
        url: '/news/profile/deletePic/',
        success: function () {
            $('#profile-pic').attr("src", "/static/news/blank-profile.png")
        }
    })
})

$('#profile-pic').click(function() {
    $("#img_file").click();
});

$(function () {
    $('#img_file').change(function uploadFile() {
        var picture = document.getElementById('img_file').files[0];
        var formData = new FormData();
        formData.append('img', picture);
        console.log("formdata" + formData);
        $.ajax({
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", $('input[name=csrfmiddlewaretoken]').val())
            },
            type: 'POST',
            url: '/news/profile/updatePic/',
            data: formData,
            success: function (data) {
                $('#profile-pic').attr("src", data)
            },
            cache: false,
            processData: false,
            contentType: false,
        })
    });
});


$(document).ready(function() {
    $('select').selectpicker();
});

$(function() {
    $(document.body).on("click", ".article-cat-but", function(){
        if(this && this.outerText) {
            var catToFilter = this.outerText;
            var baseEP = '/news/articles/?filter=';
            var endPoint = baseEP.concat(catToFilter);

            var filterButtonIdPrefix = 'filter-button-'
            filterButtonIdPrefix = filterButtonIdPrefix.concat(catToFilter);

            if($("#" + filterButtonIdPrefix).length) {
                return
            }

            $.ajax({
                url: endPoint,
                type: 'GET',
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", $('input[name=csrfmiddlewaretoken]').val());
                },
                success: function(result) {
                    if(result) {
                        result = JSON.parse(result)
                    }
                    if(result && result.status && result.status == 'success' && result.articles) {
                        var id = ".item-container"
                        $(id).remove()
                        result.articles.forEach(addArticles);

                        function addArticles(article) {
                            $("#articles-grid").append(
                                generateArticleHtml(article)
                            );
                        }

                        $("#article-filters-container").append('<button class="btn btn-danger article-filter-but-header" id="' + filterButtonIdPrefix + '">' + catToFilter + '</button>');
                    }
                }
            });
        }
    });

    $(document.body).on("click", ".article-filter-but-header", function(){
        if(this && this.outerText) {
            var catToFilter = this.outerText;
            var baseEP = '/news/articles/?filter=';

            var filters = $(".article-filter-but-header");

            for (i = 0; i < filters.length; i++) {
                if(filters[i].innerHTML == this.outerText) {
                    continue
                }
                if(i != 0) {
                    baseEP = baseEP.concat(", ")
                }
                baseEP = baseEP.concat(filters[i].innerHTML)
            };

            $.ajax({
                url: baseEP,
                type: 'GET',
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", $('input[name=csrfmiddlewaretoken]').val());
                },
                success: function(result) {
                    if(result) {
                        result = JSON.parse(result)
                    }
                    if(result && result.status && result.status == 'success' && result.articles) {
                        var id = ".item-container"
                        $(id).remove()
                        result.articles.forEach(addArticles);

                        function addArticles(article) {
                            $("#articles-grid").append(
                                generateArticleHtml(article)
                            );
                        }

                        var filterButtonIdPrefix = '#filter-button-'
                        filterButtonIdPrefix = filterButtonIdPrefix.concat(catToFilter);
                        $(filterButtonIdPrefix).remove()
                    }
                }
            });
        }
    });
});

$(document.body).on("click", ".sign-up", function(){
    var elements = document.getElementsByClassName("choice");
    for(let element of elements) {
        element.innerHTML = "Item: " + element.innerHTML;
    }
});

$('#password, #password2').on('keyup', function () {
        if ($('#password').val() === $('#password2').val()) {
            $('#message').html('')
        } else
            $('#message').html('Not Matching').css('color', 'red');
    });

$('#signup-form').on('submit', function(e) {
    e.preventDefault();
    const data = {
        "firstname": $('input[id=su-first-name]').val(),
        "surname": $('input[id=su-last-name]').val(),
        "username": $('input[id=su-username]').val(),
        "email": $('input[id=signup-email]').val(),
        "dob": $('input[id=su-dob]').val(),
        "password": $('input[id=password]').val(),
    };
    $.ajax({
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name=csrfmiddlewaretoken]').val());
        },
        type: 'POST',
        url: '/news/signup/',
        success: function () {
            window.location.href = '/news/login/'
        },
        error: function () {
            var alert = $("#error-alert");
            alert.removeAttr('hidden');
            alert.html("Sign up fail, please try again");
            alert.fadeTo(2000, 500).slideUp(500, function() {
                alert.slideUp(500);
            });
        },
        data: data,
        dataType: 'json',
    })
});


$(document.body).on("click", ".article-header", function(){
    $("#news-modal-title").text(this.parentElement.innerText);
    var articleContent = $(this).parent().parent().find('.article-content').html();
    var ident = $(this).parent().parent().find('#article-ident').html();

    var baseEP = '/news/reactions/?article=';
    baseEP = baseEP.concat(ident);
    updateReactions(baseEP);

    baseEP = '/news/comments/?article=';
    baseEP = baseEP.concat(ident);
    updateComments(baseEP);

    $("#news-modal-content").text(articleContent);
    $("#news-modal-ident").text(ident);
    $("#denied-alert").attr("hidden", "true");
    $('.comment-add-button').text("Add Comment");
    $('#comment-add-area').val("");
    $("#news-modal").modal("show");
});

$(document.body).on("click", ".reaction-button", function(){
    var articleIdent = $('#news-modal-ident').html();

    if(this.id == "news-modal-like"){
        var baseEP = '/news/like/?article=';
    }
    else {
        var baseEP = '/news/dislike/?article=';
    }
    
    baseEP = baseEP.concat(articleIdent);

    updateReactions(baseEP)
});

const updateReactions = (baseEP) => {
    $.ajax({
        url: baseEP,
        type: 'GET',
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name=csrfmiddlewaretoken]').val());
        },
        success: function(result) {
            if(result) {
                result = JSON.parse(result)
            }
            if(result && result.status && result.status != 'fail' ) {
                var likes = result.likes - result.dislikes;
                var reactionsText = "Likes: " + likes;
                $("#news-modal-reaction").text(reactionsText);
                var button = $(".reaction-button");
                button.removeAttr("disabled");
                if(result.status == 'disable-like') {
                    var button = $(".reaction-button-like");
                    button.prop("disabled", "true");
                }
                else if(result.status == 'disable-dislike') {
                    var button = $(".reaction-button-dislike");
                    button.prop("disabled", "true");
                }
                else if(result.status == 'not logged in') {
                    button.prop("disabled", "true");
                }
            }
            else if(result && result.status) {
                var alert = $("#denied-alert");
                alert.removeAttr('hidden');
                alert.html("You have already performed a like / dislike for this article!");
                alert.fadeTo(2000, 500).slideUp(500, function() {
                    alert.slideUp(500);
                });
            } 
        }
    });
};

const updateComments = (baseEP) => {
    $.ajax({
        url: baseEP,
        type: 'GET',
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name=csrfmiddlewaretoken]').val());
        },
        success: function(result) {
            $(".comment-outer").remove()
            if(result) {
                result = JSON.parse(result)
            }
            if(result && result.status && result.status == 'success') {
                result.comments.forEach(addComment);
                function addComment(comment) {
                    var commentReplyHtmlText = '';
                    if(comment.inReplyTo && comment.inReplyTo.length){
                        commentReplyHtmlText = generateReplyHtml(comment.ident, comment.inReplyTo)
                    }
                    if(result.user == comment.user){
                        $("#comments-space").prepend(
                            '<div class="comment-outer" id="' + comment.ident + '"><div class="comment"><p>' + commentReplyHtmlText + '</p><p class="comment-text">' + comment.text + '</p></div><div class="buttons-container"><button class="action-button btn btn-danger">Delete</button><button class="action-button btn btn-warning">Edit</button></div></div>'
                        );
                    } else {
                        $("#comments-space").prepend(
                            '<div class="comment-outer" id="' + comment.ident + '"><div class="comment"><p>' + commentReplyHtmlText + '</p><p class="comment-text">' + comment.text + '</p></div><div class="buttons-container"><button class="action-button btn btn-success">Reply</button></div><p><b><i>Author</i></b>: ' + comment.user + '</p></div>'
                        );
                    }
                }
            }
            else if(result.status && result.status == "not logged in") {
                $(".comment-add-button").prop('disabled', true);
                $(".reaction-button").prop('disabled', true);
                $("#comment-add-area").prop('disabled', true);
                $("#comments-space").prepend(
                    '<div class="comment-outer" id="0000"><p><b>Please login to view comments and to like / comment</b></p></div>'
                );
            }   
        }
    });
};

const generateReplyHtml = (ident, text) => {
    return('<b id="' + ident + '-reply"><i>' + 'In reply to: ' + text + '</i></b>');
};

const generateArticleHtml = (article) => {
    return(
        '<div class="item-container bg-dark text-center text-white" id=' + article.category + '>' +
            '<div class="my-3 py-3">'+
                '<p hidden="true" id="article-ident">' + article.ident + '</p>' +
                '<div>' +
                    '<button class="link display-5 article-header">' + article.title + '</button>' +
                '</div>' +
                    '<button class="btn btn-primary article-cat-but">' + article.category + '</button>' +
                '<div class="article-content">' + article.content + '</div>' +
            '</div>' +
        '</div>'
    );
};

$(document.body).on("click", ".action-button", function(){
    var baseEP = '/news/';
    var commentId = this.parentElement.parentElement.id;
    if(this.innerText.toUpperCase() == "DELETE"){
        baseEP = baseEP + 'deletecomment/?comment=';
        baseEP = baseEP + commentId;
        $.ajax({
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", $('input[name=csrfmiddlewaretoken]').val())
            },
            url: baseEP,
            type: 'DELETE',
            success: function(result) {
                if(result) {
                    result = JSON.parse(result)
                    if(result && result.status && result.status == "success") {
                        commentId = result.commentId;
                        commentId = '#' + commentId
                        $(commentId).remove()
                        $('.comment-add-button').text("Add Comment");
                        $('#comment-add-area').val("");

                        result.replies.forEach(deleteReplyComments);

                        function deleteReplyComments(ident) {
                            commentId = '#' + ident
                            $(commentId).remove()
                        }        
                    }
                }
            }
        });
    } else if(this.innerText.toUpperCase() == "REPLY"){
        $('.comment-add-button').text("Submit Reply");
        $("#comment-ident").remove();
        $(".comments-panel").append(
            '<p id="comment-ident" hidden="true">' + commentId + '</p>'
        );
    } else if(this.innerText.toUpperCase() == "EDIT"){
        var commentText = $(this).parent().parent().find('.comment-text').html();
        $('#comment-add-area').val(commentText);
        $('.comment-add-button').text("Submit Edit");
        $("#comment-ident").remove();
        $(".comments-panel").append(
            '<p id="comment-ident" hidden="true">' + commentId + '</p>'
        );
    }
});

$(document.body).on("click", ".comment-add-button", function(){
    var commentText = $('#comment-add-area').val();

    if(commentText && commentText.length){
        if(this.outerText == "Submit Edit"){
            var commentIdent = $('#comment-ident').html();
            var baseEP = '/news/editcomment/';
            editComment(baseEP, commentText, commentIdent)
        } else if(this.outerText == "Add Comment"){
            var articleIdent = $('#news-modal-ident').html();
            var baseEP = '/news/comment/';
            comment(baseEP, commentText, articleIdent, '')
        } else if(this.outerText == "Submit Reply"){
            var commentIdent = $('#comment-ident').html();
            var articleIdent = $('#news-modal-ident').html();
            var baseEP = '/news/comment/';
            comment(baseEP, commentText, articleIdent, commentIdent)
        }
    }
});

const comment = (baseEP, commentText, ident, inReplyTo) => {
    $.ajax({
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name=csrfmiddlewaretoken]').val())
        },
        url: baseEP,
        type: 'POST',
        data: {
            "commentText": commentText,
            "ident": ident,
            "inReplyTo": inReplyTo
        },
        success: function(result) {
            if(result) {
                result = JSON.parse(result)
                if(result && result.status && result.status == "success") {
                    var commentReplyHtmlText = '';
                    if(result.inReplyTo && result.inReplyTo.length){
                        commentReplyHtmlText = generateReplyHtml(result.commentId, result.inReplyTo)
                    }

                    commentAdded = result.commentAdded
                    commentId = result.commentId

                    $("#comments-space").prepend(
                        '<div class="comment-outer" id="' + commentId + '"><div class="comment"><p>' + commentReplyHtmlText + '</p><p class="comment-text">' + commentAdded + '</p></div><div class="buttons-container"><button class="action-button btn btn-danger">Delete</button><button class="action-button btn btn-warning">Edit</button></div></div>'
                    );

                    $('.comment-add-button').text("Add Comment");
                    $('#comment-add-area').val("");
                }
            }
        }
    });
};

const editComment = (baseEP, commentText, ident) => {
    $.ajax({
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", $('input[name=csrfmiddlewaretoken]').val())
        },
        url: baseEP,
        type: 'PUT',
        data: {
            'commentText': commentText,
            'ident': ident
        },
        success: function(result) {
            if(result) {
                result = JSON.parse(result)
                if(result && result.status && result.status == "success") {
                    commentId = result.commentId;
                    commentId = '#'.concat(commentId);
                    var comment = $(commentId).find('.comment-text');
                    comment.text(result.newText)
                    $('.comment-add-button').text("Add Comment");
                    $('#comment-add-area').val("");

                    result.replies.forEach(changeReplyCommentsHeader);

                    function changeReplyCommentsHeader(ident) {
                        replyHeaderId = '#' + ident + '-reply'
                        $(replyHeaderId).replaceWith(generateReplyHtml(ident, commentText))
                    }  
                }
            }
        }
    });
};
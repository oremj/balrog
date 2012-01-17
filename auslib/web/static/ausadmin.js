function getHTML(url) {
    return $.get(url, {'format': 'html'})
    .error(function(req, code, error) {
        alert(req);
        alert(code);
        alert(error);
    });
}

function getFullURL(url) {
    return SCRIPT_ROOT + url;
}

function getUsers() {
    return getHTML(getFullURL('/users'));
}

function getUserPermissions(username) {
    return getHTML(getFullURL('/users/' + username + '/permissions'));
}

function getNewUserPermission(username) {
    return getHTML(getFullURL('/users/' + username + '/permissions/new'));
}

function addUsers(element) {
    getUsers()
    .success(function(data) {
        element.append(data);
    });
}

function addUserPermissions(username, element) {
    getUserPermissions(username)
    .success(function(data) {
        element.append(data);
    });
}

function addNewUserPermission(username, element) {
    getNewUserPermission(username)
    .success(function(data) {
        element.prepend(data);
   });
}

function redirect(page, args) {
    window.location.assign(page + '?' + $.param(args));
}

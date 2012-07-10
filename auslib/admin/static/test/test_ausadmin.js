asyncTest("testAddNewPermission", 1, function() {
    var ret = document.createElement('div');
    addNewPermission('foo', 'admin', null, ret)
    .complete(function(response, text) {
        ok(response.status == 201, "got incorrect response from the server (" + response.status + ") instead of 201");
        console.log(ret.innerHTML);
        start();
    });
});

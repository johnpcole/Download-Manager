//Sets up the page load

$(document).ready(function ()
{
    $('#ajaxloader').hide();
});


function switchView()
{
    var newurl = "/Monitor=" + getNewView();
    window.location.replace(newurl);
};


function getNewView()
{
    var pathname = window.location.pathname;
    var currentview = pathname.substring(9);
    if (currentview == 'Recent') {
        var newview = 'Latest';
    } else {
        var newview = 'Recent';
    };
    return newview;
};




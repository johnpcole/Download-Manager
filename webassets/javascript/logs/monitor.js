//Sets up the page load

$(document).ready(function ()
{
    $('#ajaxloader').hide();
    if (getCurrentView() == "None") {
        switchView();
    };
});


function switchView()
{
    changeButtonState("SwitchView", "Disable");
    var newurl = "/Monitor=" + getNewView();
    window.location.replace(newurl);
};


function getNewView()
{
    if (getCurrentView() == 'Latest') {
        var newview = 'Recent';
    } else {
        var newview = 'Latest';
    };
    return newview;
};


function getCurrentView()
{
    var pathname = window.location.pathname;
    var currentview = pathname.substring(9);
    return currentview;
};
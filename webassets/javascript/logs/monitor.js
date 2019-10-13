//Sets up the page load

$(document).ready(function ()
{
    $('#ajaxloader').hide();
    switchView();
});



// Ajax call for all torrent data

function switchView()
{
    changeButtonState("SwitchView", "Disable");
    var newview = getNewView()
    $.ajax({
        url: 'MonitorData',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'timespan': newview}),
        dataType:'json',
        success: function(data)
        {
            alert(data.monitorstats);
            updateMonitorCharts(data.monitorstats);
            rerenderText("CurrentView", newview);
            changeButtonState("SwitchView", "Enable");
        }
    });
};


function getNewView()
{
    if (getText("CurrentView") == 'Latest') {
        var newview = 'Recent';
    } else {
        var newview = 'Latest';
    };
    return newview;
};




function updateMonitorCharts(dataset)
{
    var arrayLength = dataset.length;
    alert(arrayLength);
    for (var i = 0; i < arrayLength; i++) {
        alert(dataset[i]);
    };
};

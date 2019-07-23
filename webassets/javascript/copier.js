//Sets up the refresh when the page loads

$(document).ready(function ()
{
    $('#adddialog').hide();
    // Refresh the tiles every ten seconds.
    setInterval(function()
    {
        if ('Hidden' == 'Hidden') {
            updateCopierList('Refresh');
        };
    }, 1000);

    $('#ajaxloader').hide();
});



// Ajax call for all torrent data

function updateCopierList(bulkaction)
{
    $.ajax({
        url: 'UpdateCopierList',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'bulkaction': bulkaction}),
        dataType:'json',
        success: function(data)
        {
            updateAllCopierTiles(data.torrents);
        }
    });
};




function updateAllCopierTiles(copydatalist)
{
    $.each(copydatalist, function(index)
    {
        var dataitem = copydatalist[index];
        updateCopierTileColour('CopyItem_'+dataitem.copyid, dataitem.status);
        rerenderImage('Icon_'+dataitem.copyid, 'copystate_'+dataitem.status, 'gif')
    });
};


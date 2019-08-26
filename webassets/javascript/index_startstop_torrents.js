
// Ajax call for to start/stop all torrents

function performBulkAction(bulkaction)
{
    $.ajax({
        url: 'PerformBulkTorrentAction',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'bulkaction': bulkaction}),
        dataType:'json',
        success: function(data)
        {
        }
    });
};



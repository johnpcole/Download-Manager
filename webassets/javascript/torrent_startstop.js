
// Ajax call for starting/stopping torrent

function performTorrentAction(action)
{
    $.ajax({
        url: 'PerformTorrentAction',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'torrentid':getCurrentTorrentId(), 'torrentaction':action}),
        dataType:'json',
        success: function(data)
        {
        }
    });
};

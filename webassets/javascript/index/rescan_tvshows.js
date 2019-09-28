
// Ajax call for to rescan tvshows

function rescanTVShows()
{
    $.ajax({
        url: 'PerformTVShowRescan',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'bulkaction': 'rescan tv shows'}),
        dataType:'json',
        success: function(data)
        {
        }
    });
};



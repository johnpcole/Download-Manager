
// Ajax call for to rescan tvshows

function rescanTVShows()
{
    updateRefreshFoldersButton('incomplete');
    $.ajax({
        url: 'PerformTVShowRescan',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'bulkaction': 'rescan tv shows'}),
        dataType:'json',
        success: function(data)
        {
            updateCopierButton(data.copyqueuestate);
            updateRefreshFoldersButton(data.refreshfolderstate);
        }
    });
};



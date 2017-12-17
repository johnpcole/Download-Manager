//Sets up the refresh when the page loads

$(document).ready(function ()
{
    $('#adddialog').hide();
    // Refresh the tiles every minute.
    setInterval(function()
    {
        if (getAreaState('adddialog') == 'Hidden') {
            updateTorrentsList('Refresh');
        };
    }, 10000);

    $('#ajaxloader').hide();
});



// Ajax call for all torrent data

function updateTorrentsList(bulkaction)
{
    $.ajax({
        url: 'UpdateTorrentsList',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'bulkaction': bulkaction}),
        dataType:'json',
        success: function(data)
        {
            updateAllTorrentTiles(data.torrents);
            updateStats(data.stats);
        }
    });
};




function updateAllTorrentTiles(torrentdatalist)
{
    $.each(torrentdatalist, function(index)
    {
        updateTorrentTile(torrentdatalist[index]);
    });
};



// Update the displayed data

function updateTorrentTile(dataitem)
{
    tid = dataitem.torrentid
    rerenderImage("StatusIcon-"+tid, "status_"+dataitem.status);
    updateTorrentTileColour("Torrent-"+tid, "contenttile", dataitem.status);
    rerenderText("Progress-"+tid, dataitem.progress)
};



// Update stats

function updateStats(stats)
{
    rerenderText('downloadneedle', '<line x1="'+stats.d.ho+'" y1="'+stats.d.vo+'" x2="'+stats.d.hf+'" y2="'+stats.d.vf+'" />');
    rerenderText('uploadneedle', '<line x1="'+stats.u.ho+'" y1="'+stats.u.vo+'" x2="'+stats.u.hf+'" y2="'+stats.u.vf+'" />');
    rerenderText('spaceneedle', '<line x1="'+stats.s.ho+'" y1="'+stats.s.vo+'" x2="'+stats.s.hf+'" y2="'+stats.s.vf+'" />');
    rerenderText('tempneedle', '<line x1="'+stats.t.ho+'" y1="'+stats.t.vo+'" x2="'+stats.t.hf+'" y2="'+stats.t.vf+'" />');
};
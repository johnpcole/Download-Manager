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
    rerenderText('downloadneedle', '<line x1="'+stats.downloadspeed.ho+'" y1="'+stats.downloadspeed.vo+'" x2="'+stats.downloadspeed.hf+'" y2="'+stats.downloadspeed.vf+'" />');
    rerenderText('uploadneedle', '<line x1="'+stats.uploadspeed.ho+'" y1="'+stats.uploadspeed.vo+'" x2="'+stats.uploadspeed.hf+'" y2="'+stats.uploadspeed.vf+'" />');
    rerenderText('spaceneedle', '<line x1="'+stats.space.ho+'" y1="'+stats.space.vo+'" x2="'+stats.space.hf+'" y2="'+stats.space.vf+'" />');
    rerenderText('tempneedle', '<line x1="'+stats.temperature.ho+'" y1="'+stats.temperature.vo+'" x2="'+stats.temperature.hf+'" y2="'+stats.temperature.vf+'" />');
    rerenderText('innerhider', '<circle cx="60.5" cy="61" r="49.5" stroke-dasharray="'+stats.activedownloads.fill+' '+stats.activedownloads.gap+'" stroke-dashoffset="'+stats.activedownloads.offset+'" /><circle cx="60.5" cy="61" r="36.5" stroke-dasharray="'+stats.activeuploads.fill+' '+stats.activeuploads.gap+'" stroke-dashoffset="'+stats.activeuploads.offset+'" />');
    rerenderText('outerhider', '<circle cx="60.5" cy="61" r="49.5" stroke-dasharray="'+stats.downloadcount.fill+' '+stats.downloadcount.gap+'" stroke-dashoffset="'+stats.downloadcount.offset+'" /><circle cx="60.5" cy="61" r="36.5" stroke-dasharray="'+stats.uploadcount.fill+' '+stats.uploadcount.gap+'" stroke-dashoffset="'+stats.uploadcount.offset+'" />');
};
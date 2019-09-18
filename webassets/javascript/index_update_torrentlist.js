//Sets up the refresh when the page loads

$(document).ready(function ()
{
    $('#adddialog').hide();
    // Refresh the tiles every minute.
    setInterval(function()
    {
        if (getAreaState('adddialog') == 'Hidden') {
            updateTorrentsList();
        };
    }, 5000);

    $('#ajaxloader').hide();
});



// Ajax call for all torrent data

function updateTorrentsList()
{
    $.ajax({
        url: 'UpdateTorrentsList',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'bulkaction': 'refresh'}),
        dataType:'json',
        success: function(data)
        {
            updateAllTorrentTiles(data.torrents);
            updateStats(data.stats);
            updateCopierButton(data.copyqueuestate);
        }
    });
};






function updateAllTorrentTiles(torrentdatalist)
{
    $.each(torrentdatalist, function(index)
    {
        if (doesAreaExist("Torrent-"+torrentdatalist[index].torrentid) == "Yes") {
            updateTorrentTile(torrentdatalist[index]);
        } else {
            window.location.replace("/");
        };
    });
};




// Update the displayed data

function updateTorrentTile(dataitem)
{
    tid = dataitem.torrentid
    rerenderImage("StatusIcon-"+tid, "status_"+dataitem.status, 'png');
    updateTorrentTileColour("Torrent-"+tid, dataitem.status);
    rerenderText("Progress-"+tid, dataitem.progress)
};



// Update stats

function updateStats(stats)
{
    updateIndexBannerTileColour(stats.networkstatus);
    updateNeedleMeter('downloadneedle', stats.downloadspeed);
    updateNeedleMeter('uploadneedle', stats.uploadspeed);
    updateNeedleMeter('spaceneedle', stats.space);
    updateNeedleMeter('tempneedle', stats.temperature);
    updateBlockMeter('innerhider', stats.activedownloads, stats.activeuploads);
    updateBlockMeter('outerhider', stats.downloadcount, stats.uploadcount);
};

function updateNeedleMeter(needlename, n)
{
    rerenderText(needlename, '<line x1="'+n.ho+'" y1="'+n.vo+'" x2="'+n.hf+'" y2="'+n.vf+'" />');
};

function updateBlockMeter(hidername, n, m)
{
    rerenderText(hidername, '<circle cx="60.5" cy="61" r="49.5" stroke-dasharray="'+n.fill+' '+n.gap+'" stroke-dashoffset="'+n.offset+'" /><circle cx="60.5" cy="61" r="36.5" stroke-dasharray="'+m.fill+' '+m.gap+'" stroke-dashoffset="'+m.offset+'" />');
};

// Update copier button

function updateCopierButton(copyqueuestate)
{
    rerenderAnimatedImage('ViewCopier_Overlay', 'copyoverlay_'+copyqueuestate, 'gif')
};



//Sets up the refresh when the page loads

$(document).ready(function ()
{
    $('#copydialog').hide();
    $('#deletedialog').hide();
    var torrentstatus = getImageName('Status');
    updateStartStopButtons(torrentstatus, 'page_load_dummy_status');
    updateCopyButton(torrentstatus, getImageName('TorrentType'), getImageName('Copy_Overlay'));
    updateDeleteButton(getImageName('Copy_Overlay'));
    updateEditButton();
    changeAreasState('readmodebuttons', 'Show');

    // Refresh the tiles every five seconds.
    setInterval(function()
    {
        if ((getAreaState('copydialog') == 'Hidden') && (getAreaState('deletedialog') == 'Hidden')) {
            updateTorrentState();
        };
    }, 5000);

    $('#ajaxloader').hide();
});


// Return the current torrent id

function getCurrentTorrentId()
{
    var pathname = window.location.pathname;
    var torrentid = pathname.substring(9);
    return torrentid;
};


// Ajax call for all torrent downloading data

function updateTorrentState()
{
    $.ajax({
        url: 'UpdateTorrent',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'torrentid':getCurrentTorrentId()}),
        dataType:'json',
        success: function(data)
        {
            if (data.selectedtorrent.filechangealert == true) {
                window.location.replace("/Torrent="+getCurrentTorrentId());
            } else {
                updateTorrentStateDisplay(data.selectedtorrent, data.copyqueuestate);
            };
        }
    });
};


// Update the displayed data

function updateTorrentStateDisplay(dataitem, copyqueuestate)
{
    var oldstatus = getImageName('Status');
    rerenderImage("Status", "torrentstatuses/"+dataitem.status, 'png');
    updateTorrentTileColour("TorrentBanner", dataitem.status);
    rerenderText("Progress", dataitem.progress);
    updateStartStopButtons(dataitem.status, oldstatus);
    updateCopyButton(dataitem.status, getImageName('TorrentType'), copyqueuestate);
    updateDeleteButton(copyqueuestate);
};



//Sets up the refresh when the page loads

$(document).ready(function ()
{
    $('#copydialog').hide();
    $('#deletedialog').hide();
    var torrentstatus = getImageName('Status').substr(7);
    updateStartStopButtons(torrentstatus, getText('initialactionstate'));
    updateCopyButton(torrentstatus, getImageName('TorrentType').substr(5), getImageName('Copy_Overlay').substr(12));
    updateDeleteButton(getImageName('Copy_Overlay').substr(12));
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
                updateTorrentStateDisplay(data.selectedtorrent, data.copyqueuestate, data.actionqueuestate);
            };
        }
    });
};


// Update the displayed data

function updateTorrentStateDisplay(dataitem, copyqueuestate, actionstate)
{
    rerenderImage("Status", "status_"+dataitem.status, 'png');
    updateTorrentTileColour("TorrentBanner", dataitem.status);
    rerenderText("Progress", dataitem.progress);
    updateStartStopButtons(dataitem.status), actionstate;
    updateCopyButton(dataitem.status, getImageName('TorrentType').substr(5), copyqueuestate);
    updateDeleteButton(copyqueuestate);
};



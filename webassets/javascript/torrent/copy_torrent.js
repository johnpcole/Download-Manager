// Invoke Torrent File Copy

function copyTorrent()
{
    $('#copydialog').show();
};


// Confirm Copy

function confirmCopy()
{
    $.ajax({
        url: 'CopyTorrent',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'copyinstruction':getCurrentTorrentId()}),
        dataType:'json',
        beforeSend: function() {
            $('#ajaxloader').show();
        },
        success: function(data){
            closeCopyDialog();
            updateCopyButton(getImageName('Status'), getImageName('TorrentType'), 'incomplete');
            updateDeleteButton(getImageName('Copy_Overlay'));
            $('#ajaxloader').hide();
        }
    });
};


// Re-population of copy dialog following reconfiguration

function populateCopyDialog(copydata)
{
    var outputtext = '';
    $.each(copydata, function(index)
    {
        var currentitem = copydata[index];
        outputtext = outputtext + '<div class="dialogitemmax">' + currentitem + '</div>';
    });
    rerenderText('dialogcontent', outputtext);
};


// Close torrent copy dialog

function closeCopyDialog()
{
    //clearInterval(copycounter);
    $('#copydialog').hide();
};





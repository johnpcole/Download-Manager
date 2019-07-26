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
            rerenderText('copyqueuestate', 'Incomplete')
            updateCopyButton(getImageName('Status').substr(7), getImageName('TorrentType').substr(5), getImageName('Copy_Overlay').substr(12));
            updateDeleteButton(getImageName('Copy_Overlay').substr(12));
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




